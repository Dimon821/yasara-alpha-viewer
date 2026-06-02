import os
import json
import numpy as np
import sys

# =========================================================
# FORCE GUI BACKEND
# =========================================================
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import filedialog, Tk  

# =========================================================
# YASARA MODULE PATH ALLOCATION
# =========================================================
yasara_root = r"C:\Users\swage\Downloads\yasara"

sys.path.insert(0, os.path.join(yasara_root, "pym"))
sys.path.insert(0, os.path.join(yasara_root, "plg"))
sys.path.insert(0, r"C:\Users\swage\yasara_alpha_viewer\yasara-alpha-viewer")

try:
    import yasaramodule
    print(f"SUCCESS: Loaded module from -> {yasaramodule.__file__}")
except ImportError:
    print("Warning: yasaramodule could not be loaded. Running in visualization-only mode.")
    yasaramodule = None

# =========================================================
# CONFIGURATION & GLOBAL STATE
# =========================================================
cfg = {
    "dataset_dir": r"C:\Users\swage\Downloads\Tyrosine-protein phosphatase non-receptor type substrate 1"
}

current_cif_path = None
current_json_path = None
plddt_data = None
pae_data = None

# Track current viewing mode ("plddt" or "pae") and focus point
current_view_mode = "plddt"
current_pae_focus_residue = 1

# =========================================================
# DATA SELECTION & LOADING ENGINE
# =========================================================
def load_from_directory(folder):
    cif_files = []
    json_files = []

    for root_dir, _, files in os.walk(folder):
        for f in files:
            lf = f.lower()
            full_path = os.path.join(root_dir, f)
            if lf.endswith(".cif"):
                cif_files.append(full_path)
            elif lf.endswith(".json"):
                json_files.append(full_path)

    if not cif_files or not json_files:
        raise ValueError(f"CRITICAL: Missing either .cif or .json files inside: {folder}")

    if len(cif_files) == 1 and len(json_files) == 1:
        return cif_files[0], json_files[0]

    cif_map = {}
    for cp in cif_files:
        base = os.path.basename(cp).lower()
        if "-model_" in base:
            key = base.split("-model_")[0]
            cif_map[key] = cp
        elif "model_" in base:
            try:
                key = base.split("model_")[1].split(".")[0]
                cif_map[key] = cp
            except:
                pass

    for jp in json_files:
        base = os.path.basename(jp).lower()
        if "-predicted_aligned_error_" in base:
            key = base.split("-predicted_aligned_error_")[0]
            if key in cif_map:
                return cif_map[key], jp
        elif "full_data_" in base:
            try:
                key = base.split("full_data_")[1].split(".")[0]
                if key in cif_map:
                    return cif_map[key], jp
            except:
                pass

    return sorted(cif_files)[0], sorted(json_files)[0]


def parse_plddt_from_cif(cif_path):
    with open(cif_path, 'r') as f:
        lines = f.readlines()
        
    atom_site_cols = []
    plddt_dict = {}
    in_atom_site_loop = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('loop_'):
            in_atom_site_loop = False
            atom_site_cols = []
            continue
        if line.startswith('_atom_site.'):
            in_atom_site_loop = True
            atom_site_cols.append(line)
            continue
        if in_atom_site_loop and (line.startswith('ATOM') or line.startswith('HETATM')):
            parts = line.split()
            try:
                b_idx = next(i for i, col in enumerate(atom_site_cols) if 'B_iso_or_equiv' in col)
                seq_idx = next(i for i, col in enumerate(atom_site_cols) if 'label_seq_id' in col)
                res_num = int(parts[seq_idx])
                b_factor = float(parts[b_idx])
                plddt_dict[res_num] = b_factor
            except (StopIteration, ValueError, IndexError):
                pass
                
    if plddt_dict:
        max_res = max(plddt_dict.keys())
        plddt_array = [plddt_dict.get(i, 0.0) for i in range(1, max_res + 1)]
        return np.array(plddt_array)
    return None


def parse_alphafold_json(json_path, cif_path=None):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        data = data[0]
        
    pae = data.get("predicted_aligned_error") or data.get("pae")
    plddt = data.get("plddt")
    
    if pae is None:
        raise KeyError("Could not locate 'predicted_aligned_error' or 'pae' arrays inside the target JSON file.")
        
    if plddt is None and cif_path is not None:
        print("Notice: pLDDT array missing from JSON. Extracting values from CIF coordinate B-factors...")
        plddt = parse_plddt_from_cif(cif_path)
        
    if plddt is None:
        raise KeyError("Could not locate pLDDT data within the JSON file or the matching CIF structure coordinates.")
        
    return np.array(plddt), np.array(pae)

# =========================================================
# COLOR ENGINE
# =========================================================
def generate_yasara_ranges(res_list):
    if not res_list: return ""
    ints = sorted(list(set([int(x) for x in res_list])))
    
    ranges = []
    start = end = ints[0]
    
    for i in ints[1:]:
        if i == end + 1:
            end = i
        else:
            ranges.append(f"{start}-{end}" if start != end else str(start))
            start = end = i
            
    ranges.append(f"{start}-{end}" if start != end else str(start))
    return " ".join(ranges)


def push_colors_to_yasara(color_groups):
    """Safely batches range requests into YASARA execution calls"""
    if yasaramodule is None:
        return
    for color_name, residues in color_groups.items():
        if not residues:
            continue
        range_string = generate_yasara_ranges(residues)
        try:
            yasaramodule.run(f"ColorRes Res {range_string}, {color_name}")
        except Exception as e:
            print(f"YASARA Color Mapping Communication error: {e}")


def apply_plddt_view():
    global current_view_mode
    current_view_mode = "plddt"
    print("Applying pLDDT Confidence Structural View...")
    
    groups = {"Red": [], "Yellow": [], "Cyan": [], "Blue": []}
    for res_idx, score in enumerate(plddt_data):
        res_num = res_idx + 1
        if score < 50: groups["Red"].append(res_num)
        elif score < 70: groups["Yellow"].append(res_num)
        elif score < 90: groups["Cyan"].append(res_num)
        else: groups["Blue"].append(res_num)
        
    push_colors_to_yasara(groups)


def apply_pae_view(focus_res):
    global current_view_mode, current_pae_focus_residue
    current_view_mode = "pae"
    current_pae_focus_residue = focus_res
    
    # Bound check the index array space
    idx = max(0, min(focus_res - 1, pae_data.shape[0] - 1))
    print(f"Applying PAE Alignment View relative to Focus Residue: {idx + 1}")
    
    # Extract the 1D error profile array slice 
    error_slice = pae_data[idx]
    
    groups = {"DarkGreen": [], "Green": [], "Yellow": [], "Orange": [], "Red": []}
    for res_idx, error in enumerate(error_slice):
        res_num = res_idx + 1
        if error <= 5.0: groups["DarkGreen"].append(res_num)
        elif error <= 10.0: groups["Green"].append(res_num)
        elif error <= 15.0: groups["Yellow"].append(res_num)
        elif error <= 25.0: groups["Orange"].append(res_num)
        else: groups["Red"].append(res_num)
        
    push_colors_to_yasara(groups)

# =========================================================
# GRAPHICS ENGINE & CONTROLS
# =========================================================
fig, (ax_pae, ax_plddt) = plt.subplots(2, 1, figsize=(7, 8))
fig.subplots_adjust(hspace=0.6, bottom=0.15)

# Track optional horizontal selection overlay lines on the canvas plots
pae_line_h = None
pae_line_v = None

def render_plots():
    global plddt_data, pae_data, pae_line_h, pae_line_v
    ax_pae.clear()
    ax_plddt.clear()
    
    # 1. PAE Matrix Panel
    ax_pae.imshow(pae_data, cmap='Blues_r', vmin=0, vmax=30, aspect='equal')
    protein_name = os.path.basename(os.path.dirname(current_cif_path))
    ax_pae.set_title(f"PAE Matrix: {protein_name}\n(Click anywhere to map errors relative to that residue)", pad=12, fontsize=10, weight='bold')
    ax_pae.set_xlabel("Scored Residue", labelpad=8)
    ax_pae.set_ylabel("Predicted Residue", labelpad=8)
    
    # Render indicators at selection intersection
    focus_idx = current_pae_focus_residue - 1
    pae_line_h = ax_pae.axhline(focus_idx, color='magenta', linestyle='--', alpha=0.7, visible=(current_view_mode == "pae"))
    pae_line_v = ax_pae.axvline(focus_idx, color='magenta', linestyle='--', alpha=0.7, visible=(current_view_mode == "pae"))
    
    # 2. pLDDT Confidence Profile Panel
    residues = np.arange(1, len(plddt_data) + 1)
    ax_plddt.plot(residues, plddt_data, color='#1f77b4', linewidth=1.5)
    ax_plddt.set_title("pLDDT Confidence Profile", pad=12)
    ax_plddt.set_xlim(1, len(plddt_data))
    ax_plddt.set_ylim(0, 105)
    
    ax_plddt.axhline(90, color='blue', linestyle=':', alpha=0.5)
    ax_plddt.axhline(70, color='cyan', linestyle=':', alpha=0.5)
    ax_plddt.axhline(50, color='orange', linestyle=':', alpha=0.5)
    
    fig.canvas.draw_idle()


def on_canvas_click(event):
    """Intercept clicks on the upper PAE matrix plot to change structure views"""
    if event.inaxes != ax_pae or event.xdata is None or event.ydata is None:
        return
        
    # Get the residue index that was clicked
    clicked_residue = int(round(event.xdata)) + 1
    
    # Adjust indicator state
    if pae_line_h and pae_line_v:
        pae_line_h.set_ydata([event.ydata, event.ydata])
        pae_line_v.set_xdata([event.xdata, event.xdata])
        pae_line_h.set_visible(True)
        pae_line_v.set_visible(True)
        
    apply_pae_view(clicked_residue)
    fig.canvas.draw_idle()


def reset_model():
    global current_cif_path
    if yasaramodule is None:
        return
        
    try:
        print(f"Loading structure inside YASARA: {os.path.basename(current_cif_path)}")
        yasaramodule.run("Clear")
        yasaramodule.run(f"LoadCIF {current_cif_path}")
        yasaramodule.run("Style Ribbon")
        
        if current_view_mode == "plddt":
            apply_plddt_view()
        else:
            apply_pae_view(current_pae_focus_residue)
    except Exception as initial_error:
        print("YASARA link is idle or not open. Attempting explicit application launch...")
        try:
            yasaramodule.info.mode = 'gph'
            yasaramodule.run("Clear")
            yasaramodule.run(f"LoadCIF {current_cif_path}")
            yasaramodule.run("Style Ribbon")
            apply_plddt_view()
        except Exception as hardware_error:
            print(f"Could not interact with or launch YASARA window binary: {hardware_error}")


def handle_change_dataset(event):
    global current_cif_path, current_json_path, plddt_data, pae_data
    print("\nOpening folder prompt...")
    
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True) 
    
    chosen_dir = filedialog.askdirectory(
        initialdir=os.path.dirname(cfg["dataset_dir"]),
        title="Select AlphaFold Protein Dataset Directory"
    )
    root.destroy()
    
    if not chosen_dir:
        print("Dataset swapping canceled.")
        return

    print(f"Switching pipeline target to: {chosen_dir}")
    try:
        new_cif, new_json = load_from_directory(chosen_dir)
        new_plddt, new_pae = parse_alphafold_json(new_json, new_cif)
        
        current_cif_path = new_cif
        current_json_path = new_json
        plddt_data = new_plddt
        pae_data = new_pae
        cfg["dataset_dir"] = chosen_dir
        
        render_plots()
        reset_model()
        print("Dataset swap complete.")
    except Exception as error:
        print(f"Failed to load selected directory structure: {error}")

# =========================================================
# MATPLOTLIB WIDGET INTERACTION INTERFACES
# =========================================================
ax_btn1 = fig.add_axes([0.15, 0.03, 0.2, 0.05])
ax_btn2 = fig.add_axes([0.40, 0.03, 0.2, 0.05])
ax_btn3 = fig.add_axes([0.65, 0.03, 0.2, 0.05])

btn1 = Button(ax_btn1, 'pLDDT View')
btn2 = Button(ax_btn2, 'PAE View (Default)')
btn3 = Button(ax_btn3, 'Change Dataset')

# Connect interaction handlers
btn1.on_clicked(lambda event: [apply_plddt_view(), pae_line_h.set_visible(False) if pae_line_h else None, pae_line_v.set_visible(False) if pae_line_v else None, fig.canvas.draw_idle()])
btn2.on_clicked(lambda event: [apply_pae_view(current_pae_focus_residue), pae_line_h.set_visible(True) if pae_line_h else None, pae_line_v.set_visible(True) if pae_line_v else None, fig.canvas.draw_idle()])
btn3.on_clicked(handle_change_dataset) 

# Bind mouse click listener event directly onto the Matplotlib window canvas
fig.canvas.mpl_connect('button_press_event', on_canvas_click)

# =========================================================
# APPLICATION INITIALIZATION ENGINE
# =========================================================
if __name__ == "__main__":
    print(f"Current Matplotlib Backend: {matplotlib.get_backend()}")
    
    current_cif_path, current_json_path = load_from_directory(cfg["dataset_dir"])
    plddt_data, pae_data = parse_alphafold_json(current_json_path, current_cif_path)
    
    print("Initializing layout canvases...")
    render_plots()
    reset_model()
    
    print("Displaying GUI Window. Close the window to exit script execution.")
    plt.show(block=False)
    
    while plt.fignum_exists(fig.number):
        plt.pause(0.1)
        
    print("Window manually closed by user. Exiting.")