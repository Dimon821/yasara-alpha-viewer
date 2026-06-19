# ==============================================================================
# 1. PYTHON 3.12+ LEGACY DEPENDENCY COMPATIBILITY HACK
# ==============================================================================
import sys
import types
import importlib.util

if 'imp' not in sys.modules:
    imp_mock = types.ModuleType('imp')
    def find_module(name, path=None):
        spec = importlib.util.find_spec(name, path)
        if spec is None:
            raise ImportError(f"No module named '{name}'")
        return (None, spec.origin, (None, None, None))
    imp_mock.find_module = find_module
    sys.modules['imp'] = imp_mock

# ==============================================================================
# 2. MAIN APPLICATION IMPORTS
# ==============================================================================
import os
import json
import numpy as np
from pymol import cmd

try:
    from pymol.Qt import QtWidgets, QtCore
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ImportError:
    from PySide6 import QtWidgets, QtCore
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure

alpha_viewer_instance = None

# ==============================================================================
# 3. ALPHAFOLD VIEWING DASHBOARD IMPLEMENTATION
# ==============================================================================
class AlphaFoldViewer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AlphaFoldViewer, self).__init__(parent)
        self.setWindowTitle("AlphaFold 3 Advanced Dashboard")
        self.resize(1100, 750)  
        
        self.current_dataset_dir = None
        self.pae_data = None
        self.plddt_data = None
        self.current_model_name = "af_model"
        self.colorbar = None
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Path Entry Bar
        path_layout = QtWidgets.QHBoxLayout()
        self.path_input = QtWidgets.QLineEdit()
        self.path_input.setPlaceholderText("Paste AlphaFold folder path here...")
        self.btn_load = QtWidgets.QPushButton("Load Dataset")
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.btn_load)
        main_layout.addLayout(path_layout)
        
        # Mode Controls
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn1 = QtWidgets.QPushButton("Color Structure by pLDDT")
        self.btn2 = QtWidgets.QPushButton("Highlight Zoomed Selection")
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)
        main_layout.addLayout(btn_layout)
        
        # --- Matplotlib Canvas Customization ---
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.toolbar)
        
        self.ax_pae = self.figure.add_subplot(121)  
        self.ax_plddt = self.figure.add_subplot(122)  
        self.setup_blank_plots()
        
        self.btn1.clicked.connect(self.handle_mode_toggle)
        self.btn2.clicked.connect(self.trigger_zoom_highlight)
        self.btn_load.clicked.connect(self.handle_change_dataset)
        self.path_input.returnPressed.connect(self.handle_change_dataset)
        
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def setup_blank_plots(self):
        """Initializes empty plot labels and formatting rules."""
        self.ax_pae.clear()
        self.ax_pae.set_title("Predicted Aligned Error (PAE)")
        self.ax_pae.set_xlabel("Scored residue")
        self.ax_pae.set_ylabel("Aligned residue")
        
        self.ax_plddt.clear()
        self.ax_plddt.set_title("Model Confidence Profile (pLDDT)")
        self.ax_plddt.set_xlabel("Residue Position")
        self.ax_plddt.set_ylabel("pLDDT Score")
        self.ax_plddt.set_ylim(0, 105)
        self.ax_plddt.grid(True, linestyle='--', alpha=0.5)

    def parse_alphafold_json(self, json_path):
        """Safely unpacks AlphaFold 3 metrics block by block handling list wrappers."""
        with open(json_path, "r") as f:
            data = json.load(f)

        # Force unwrap if AlphaFold wrapped the main dictionary inside a 1-element list
        if isinstance(data, list):
            if len(data) > 0:
                data = data[0]
            else:
                return None, None

        if not isinstance(data, dict):
            print("PyMOL Error: Top level JSON structure is neither a standard dict nor a valid list.")
            return None, None

        # Target the AF3 specific dictionary nested blocks safely
        metrics_block = data.get("reconstructed_metrics") or data.get("model_metrics") or data

        raw_pae = metrics_block.get("pae") or metrics_block.get("pae_data")
        raw_plddt = metrics_block.get("atom_plddts") or metrics_block.get("plddt")

        return raw_pae, raw_plddt

    def reset_model(self):
        cmd.delete("all")
        if self.colorbar:
            try:
                self.colorbar.remove()
            except:
                pass
            self.colorbar = None
        self.setup_blank_plots()
        self.canvas.draw()
        self.pae_data = None
        self.plddt_data = None

    def handle_change_dataset(self):
        dir_path = self.path_input.text().strip()
        if not dir_path:
            return
            
        dir_path = os.path.expanduser(dir_path)
        if not os.path.exists(dir_path):
            print(f"PyMOL Error: Path does not exist: {dir_path}")
            return
            
        self.current_dataset_dir = dir_path
        self.reset_model()
        
        struct_path = None
        json_path = None
        
        for root, dirs, files in os.walk(dir_path):
            if "templates" in root or "msas" in root:
                continue
            files.sort()
            
            cif_models = [f for f in files if (f.endswith(".cif") or f.endswith(".pdb")) and "template" not in f.lower()]
            if cif_models and not struct_path:
                best_model = next((f for f in cif_models if "model_0" in f), cif_models[0])
                struct_path = os.path.join(root, best_model)
                
            json_files = [f for f in files if f.endswith(".json")]
            if json_files and not json_path:
                best_json = next((f for f in json_files if "full_data_0" in f), None)
                if not best_json:
                    best_json = next((f for f in json_files if "full_data" in f), None)
                if best_json:
                    json_path = os.path.join(root, best_json)

        if struct_path and json_path:
            print(f"Loading Structure: {os.path.basename(struct_path)}")
            print(f"Loading Metrics File: {os.path.basename(json_path)}")
            
            cmd.load(struct_path, self.current_model_name)
            cmd.show_as("cartoon", self.current_model_name)
            cmd.orient(self.current_model_name)
            
            raw_pae, raw_plddt = self.parse_alphafold_json(json_path)
            
            # Count internal structure Alpha Carbon count
            stored_b = []
            cmd.iterate(f"{self.current_model_name} and name CA", "stored_b.append(b)", space={'stored_b': stored_b})
            ca_count = len(stored_b)

            # --- Process PAE Data Matrix ---
            if raw_pae is not None:
                self.pae_data = np.array(raw_pae)
                if len(self.pae_data.shape) == 1:
                    n = int(np.sqrt(self.pae_data.shape[0]))
                    if n * n == self.pae_data.shape[0]:
                        self.pae_data = self.pae_data.reshape((n, n))
                
                self.ax_pae.clear()
                self.ax_pae.set_title("Predicted Aligned Error (PAE)")
                self.ax_pae.set_xlabel("Scored residue")
                self.ax_pae.set_ylabel("Aligned residue")
                
                cax = self.ax_pae.imshow(self.pae_data, cmap='bwr', vmin=0, vmax=30)
                if self.colorbar is None:
                    self.colorbar = self.figure.colorbar(cax, ax=self.ax_pae, label="Expected Position Error (Å)", orientation='horizontal', pad=0.15)
            else:
                print("Warning: PAE array parsing returned empty.")
            
            # --- Process pLDDT Profile ---
            if raw_plddt is not None:
                parsed_plddt = np.array(raw_plddt)
                if len(parsed_plddt) > ca_count and ca_count > 0:
                    self.plddt_data = np.array(stored_b)
                else:
                    self.plddt_data = parsed_plddt
            else:
                self.plddt_data = np.array(stored_b)

            if self.plddt_data is not None and len(self.plddt_data) > 0:
                if np.max(self.plddt_data) <= 1.0:
                    self.plddt_data = self.plddt_data * 100.0

                residues = np.arange(1, len(self.plddt_data) + 1)
                
                self.ax_plddt.clear()
                self.ax_plddt.set_title("Model Confidence Profile (pLDDT)")
                self.ax_plddt.set_xlabel("Residue Position")
                self.ax_plddt.set_ylabel("pLDDT Score")
                self.ax_plddt.set_ylim(0, 105)
                self.ax_plddt.grid(True, linestyle='--', alpha=0.5)
                
                self.ax_plddt.plot(residues, self.plddt_data, color='black', linewidth=1.5, alpha=0.8)
                self.ax_plddt.fill_between(residues, self.plddt_data, 90, where=(self.plddt_data >= 90), color='dodgerblue', alpha=0.3, label='Very High (pLDDT > 90)')
                self.ax_plddt.fill_between(residues, self.plddt_data, 70, where=((self.plddt_data >= 70) & (self.plddt_data < 90)), color='mediumaquamarine', alpha=0.3, label='Confident')
                self.ax_plddt.fill_between(residues, self.plddt_data, 50, where=((self.plddt_data >= 50) & (self.plddt_data < 70)), color='orange', alpha=0.3, label='Low')
                self.ax_plddt.fill_between(residues, self.plddt_data, 0, where=(self.plddt_data < 50), color='crimson', alpha=0.3, label='Very Low (< 50)')
                self.ax_plddt.legend(loc='lower left', fontsize='small')
                self.ax_plddt.set_xlim(1, len(self.plddt_data))

            self.handle_mode_toggle()
            self.figure.tight_layout()
            self.canvas.draw()
            print("Successfully loaded dual metrics display analytics panel!")
        else:
            print("Scan failed. Check directory elements.")

    def handle_mode_toggle(self):
        stored_b = []
        cmd.iterate(self.current_model_name, "stored_b.append(b)", space={'stored_b': stored_b})
        max_b = max(stored_b) if stored_b else 100
        min_lim, max_lim = (50, 90) if max_b > 1.0 else (0.5, 0.9)
        cmd.spectrum("b", "red_yellow_green_cyan_blue", self.current_model_name, minimum=min_lim, maximum=max_lim)

    def trigger_zoom_highlight(self, event=None):
        if "sele" in cmd.get_names("selections"):
            cmd.zoom("sele", buffer=2.0)
            cmd.color("yellow", "sele")

    def on_canvas_click(self, event):
        if event.xdata is None or event.ydata is None:
            return
            
        if event.inaxes == self.ax_pae and self.pae_data is not None:
            res1 = int(round(event.xdata)) + 1
            res2 = int(round(event.ydata)) + 1
            selection_query = f"({self.current_model_name} and resi {res1}) or ({self.current_model_name} and resi {res2})"
        elif event.inaxes == self.ax_plddt and self.plddt_data is not None:
            res_target = int(round(event.xdata))
            selection_query = f"{self.current_model_name} and resi {res_target}"
        else:
            return
            
        selection_name = "pae_interaction"
        cmd.select(selection_name, selection_query)
        cmd.show("sticks", selection_name)
        cmd.zoom(selection_name, buffer=5.0)
        cmd.color("magenta", selection_name)

# ==============================================================================
# 4. PYMOL INITIALIZATION AND RUNTIME TRIGGERS
# ==============================================================================
def start_alpha_viewer():
    global alpha_viewer_instance
    if alpha_viewer_instance is None:
        try:
            from pymol.qt import get_main_window
            parent = get_main_window()
        except:
            parent = None
        alpha_viewer_instance = AlphaFoldViewer(parent=parent)
        
    alpha_viewer_instance.show()
    alpha_viewer_instance.raise_()

cmd.extend("start_alpha_viewer", start_alpha_viewer)
start_alpha_viewer()