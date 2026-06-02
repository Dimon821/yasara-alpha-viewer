import sys
import os
import json
import tkinter as tk
from tkinter import filedialog

import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Button
import numpy as np

# =========================================================
# CONFIG
# =========================================================

CONFIG_FILE = "config.json"


def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"yasara_dir": "", "cif_path": "", "json_path": ""}


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)


def pick_dir(title):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return filedialog.askdirectory(title=title)


def load_from_directory(folder):
    """
    AlphaFold-aware pairing:
    model_X.cif ↔ full_data_X.json
    """

    cif_map = {}
    json_map = {}

    for root, _, files in os.walk(folder):
        for f in files:
            lf = f.lower()

            # --- CIF MODELS ---
            if lf.endswith(".cif") and "model_" in lf:
                try:
                    idx = int(lf.split("model_")[1].split(".")[0])
                    cif_map[idx] = os.path.join(root, f)
                except:
                    pass

            # --- PAE / FULL DATA JSON ---
            if lf.endswith(".json") and "full_data_" in lf:
                try:
                    idx = int(lf.split("full_data_")[1].split(".")[0])
                    json_map[idx] = os.path.join(root, f)
                except:
                    pass

    # find best available pair
    common = sorted(set(cif_map.keys()) & set(json_map.keys()))

    if not common:
        raise ValueError("No matching CIF/JSON model pairs found")

    best_idx = common[0]  # or change to best confidence later

    return cif_map[best_idx], json_map[best_idx]
# =========================================================
# LOAD DATASET
# =========================================================

cfg = load_config()

# 1. ALWAYS pick YASARA install folder FIRST (if missing)
if not cfg.get("yasara_install") or not os.path.isdir(cfg["yasara_install"]):
    cfg["yasara_install"] = pick_dir("Select YASARA INSTALLATION folder (has pym/ and plg/)")

# 2. THEN pick dataset folder
dataset_dir = pick_dir("Select AlphaFold dataset folder")

if not dataset_dir:
    raise SystemExit("No dataset selected")

cfg["dataset_dir"] = dataset_dir

save_config(cfg)

cif_path, json_path = load_from_directory(cfg["yasara_dir"])

cfg["cif_path"] = cif_path
cfg["json_path"] = json_path
save_config(cfg)

yasara_dir = cfg["yasara_dir"]

# =========================================================
# YASARA INIT
# =========================================================

sys.path.append(os.path.join(yasara_dir, "pym"))
sys.path.append(os.path.join(yasara_dir, "plg"))

from yasaramodule import *

Clear()
LoadCIF(cif_path)

# =========================================================
# LOAD PAE
# =========================================================

with open(json_path, "r") as f:
    pae_data = json.load(f)

domains = []

if isinstance(pae_data, dict):
    pae_matrix = pae_data.get("pae") or pae_data.get("predicted_aligned_error")
    domains = pae_data.get("domains", [])

else:
    pae_matrix = pae_data[0]["predicted_aligned_error"]

pae_matrix = np.array(pae_matrix)
pae_matrix = np.squeeze(pae_matrix)

total_residues = pae_matrix.shape[0]

# =========================================================
# PARSE CIF pLDDT
# =========================================================

plddt_dict = {}

with open(cif_path, "r") as f:
    for line in f:
        if line.startswith("ATOM"):
            parts = line.split()
            try:
                if parts[3] == "CA" or parts[4] == "CA":
                    res = int(parts[8])
                    val = float(parts[14])
                    plddt_dict[res] = val
            except:
                continue

sorted_res_nums = sorted(plddt_dict.keys())

if len(sorted_res_nums) == total_residues:
    plddt_profile = np.array([plddt_dict[r] for r in sorted_res_nums])
else:
    sorted_res_nums = list(range(1, total_residues + 1))
    plddt_profile = np.clip(100 - np.diag(pae_matrix) * 2.5, 0, 100)

# =========================================================
# COLOR ENGINE
# =========================================================

is_updating = False


def set_residue_colors(residue_values):
    for res, val in residue_values:
        hue = int(round((val / 100.0) * 240.0))
        run(f"BFactor Res {res} {hue}")

    run("ColorAll BFactor")


# =========================================================
# VIEWS
# =========================================================

def apply_plddt(event=None):
    values = list(zip(sorted_res_nums, plddt_profile))
    set_residue_colors(values)


def apply_pae(event=None):
    values = []

    for i, res in enumerate(sorted_res_nums):
        err = np.mean(pae_matrix[i])
        val = np.clip((err / 30.0) * 100, 0, 100)
        values.append((res, val))

    set_residue_colors(values)


def reset_model(event=None):
    apply_plddt()


# =========================================================
# ZOOM
# =========================================================

def on_xlims_change(ax):
    global is_updating
    if is_updating:
        return

    xmin, xmax = ax.get_xlim()

    x_low = max(1, min(total_residues, int(round(xmin))))
    x_high = max(1, min(total_residues, int(round(xmax))))

    if abs(x_high - x_low) <= 2:
        return

    is_updating = True

    reset_model()

    values = []

    for i in range(x_low, x_high + 1):
        err = np.mean(pae_matrix[:, i - 1])
        val = np.clip((err / 30.0) * 100, 0, 100)
        res = sorted_res_nums[i - 1]
        values.append((res, val))

    set_residue_colors(values)

    is_updating = False


# =========================================================
# DOMAIN ANNOTATION
# =========================================================

def draw_domains(ax):
    if not domains:
        return

    for d in domains:
        start = d.get("start", 0)
        end = d.get("end", 0)
        name = d.get("name", "Domain")

        ax.axvspan(start, end, alpha=0.15)
        ax.text(
            (start + end) / 2,
            1,
            name,
            rotation=90,
            ha="center",
            va="bottom",
            fontsize=8
        )


# =========================================================
# CHANGE DATASET
# =========================================================

def change_directory(event=None):
    global cfg, cif_path, json_path, pae_matrix, total_residues, domains, sorted_res_nums, plddt_profile

    folder = pick_dir("Select new dataset folder")
    if not folder:
        return

    cfg["yasara_dir"] = folder

    cif_path, json_path = load_from_directory(folder)

    cfg["cif_path"] = cif_path
    cfg["json_path"] = json_path
    save_config(cfg)

    os.execv(sys.executable, [sys.executable] + sys.argv)


# =========================================================
# INIT
# =========================================================

reset_model()

# =========================================================
# PLOT
# =========================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(7, 8.5),
    gridspec_kw={"height_ratios": [2, 1]}
)

# PAE now WHITE
cmap = LinearSegmentedColormap.from_list(
    "pae_white", ["white", "white"]
)

ax1.imshow(
    pae_matrix,
    cmap=cmap,
    origin="upper",
    vmin=0,
    vmax=30,
    extent=[1, total_residues, total_residues, 1]
)

ax1.set_title("PAE Matrix (Zoom to Recolor Structure)")

ax2.plot(sorted_res_nums, plddt_profile, color="#106dff")

ax2.axhline(90, ls=":")
ax2.axhline(70, ls=":")
ax2.axhline(50, ls=":")

ax2.set_ylim(0, 105)
ax2.set_title("pLDDT Confidence Profile")

draw_domains(ax2)

plt.tight_layout(rect=[0, 0.09, 1, 1])

# =========================================================
# BUTTONS
# =========================================================

ax_btn1 = plt.axes([0.10, 0.02, 0.22, 0.04])
ax_btn2 = plt.axes([0.40, 0.02, 0.22, 0.04])
ax_btn3 = plt.axes([0.70, 0.02, 0.22, 0.04])

btn1 = Button(ax_btn1, "pLDDT View")
btn2 = Button(ax_btn2, "PAE View")
btn3 = Button(ax_btn3, "Change Dataset")

btn1.on_clicked(reset_model)
btn2.on_clicked(apply_pae)
btn3.on_clicked(change_directory)

ax1.callbacks.connect("xlim_changed", on_xlims_change)
ax1.callbacks.connect("ylim_changed", on_xlims_change)

plt.show()