import os
import json
import numpy as np

# Import PyMOL API
from pymol import cmd

# Dynamically handle PyQt/PySide depending on environment
try:
    from PyQt5 import QtWidgets, QtCore
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
except ImportError:
    from PySide6 import QtWidgets, QtCore
    import matplotlib
    matplotlib.use('qtagg')
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

# Global reference to prevent the garbage collector from destroying the window
alpha_viewer_instance = None

class PyMOLAlphaFoldViewer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PyMOLAlphaFoldViewer, self).__init__(parent)
        self.setWindowTitle("PyMOL AlphaFold PAE & pLDDT Analyzer")
        self.resize(1000, 600)
        
        self.current_dataset_dir = None
        self.pae_data = None
        self.plddt_data = None
        self.colorbar = None  
        
        # --- UI Layout ---
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Buttons Setup
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn1 = QtWidgets.QPushButton("Color by pLDDT")
        self.btn2 = QtWidgets.QPushButton("Reset View")
        self.btn3 = QtWidgets.QPushButton("Change Dataset")
        
        btn_layout.addWidget(self.btn3)
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)
        main_layout.addLayout(btn_layout)
        
        # Matplotlib Canvas Setup (Dual Plot Layout)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)
        
        # Left Subplot: PAE Heatmap
        self.ax_pae = self.figure.add_subplot(121)
        self.setup_pae_axes()
        
        # Right Subplot: pLDDT Line Graph
        self.ax_plddt = self.figure.add_subplot(122)
        self.setup_plddt_axes()
        
        # --- Callbacks & Connections ---
        self.btn1.clicked.connect(self.handle_mode_toggle)
        self.btn2.clicked.connect(self.reset_view)
        self.btn3.clicked.connect(self.handle_change_dataset)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def setup_pae_axes(self):
        """Initializes labels for the PAE matrix."""
        self.ax_pae.set_title("Predicted Aligned Error (PAE)")
        self.ax_pae.set_xlabel("Scored residue")
        self.ax_pae.set_ylabel("Aligned residue")

    def setup_plddt_axes(self):
        """Initializes labels for the pLDDT chart."""
        self.ax_plddt.set_title("Model Confidence (pLDDT)")
        self.ax_plddt.set_xlabel("Residue position")
        self.ax_plddt.set_ylabel("pLDDT Score")
        self.ax_plddt.set_ylim(0, 105)
        self.ax_plddt.grid(True, linestyle='--', alpha=0.5)

    def select_dataset_dialog(self):
        """Opens a folder picker to select the dataset directory."""
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select AlphaFold Output Folder")
        return dir_path

    def parse_alphafold_json(self, json_path):
        """Safely extracts both PAE and pLDDT data from AlphaFold/ColabFold JSON variants."""
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            data = data[0]
            
        print("Found JSON keys:", data.keys() if isinstance(data, dict) else "List format")
            
        # Try finding the 2D PAE matrix
        pae = data.get('pae') or data.get('predicted_aligned_error') or data.get('distance')
        # Try finding the 1D pLDDT sequence
        plddt = data.get('plddt') or data.get('pLDDT') or data.get('atom_plddts')
        
        return (np.array(pae) if pae is not None else None, 
                np.array(plddt) if plddt is not None else None)

    def reset_model(self):
        """Clears PyMOL workspace and flushes both Matplotlib plots."""
        cmd.reinitialize()
        
        self.ax_pae.clear()
        self.ax_plddt.clear()
        
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None
            
        self.setup_pae_axes()
        self.setup_plddt_axes()
        self.canvas.draw()
        
        self.pae_data = None
        self.plddt_data = None

    def handle_change_dataset(self):
        """Loads structural models and syncs analytics dashboards inside PyMOL."""
        dir_path = self.select_dataset_dialog()
        if not dir_path:
            return
            
        self.current_dataset_dir = dir_path
        self.reset_model()
        
        try:
            files = os.listdir(dir_path)
        except FileNotFoundError:
            return

        struct_file = next((f for f in files if f.endswith(".pdb") or f.endswith(".cif")), None)
        # Prioritize rich data files (like full_data files) if available
        json_file = next((f for f in files if f.endswith(".json") and ("full_data" in f.lower() or "pae" in f.lower() or "scores" in f.lower() or "rank" in f.lower())), None)
        
        if struct_file and json_file:
            struct_path = os.path.join(dir_path, struct_file).replace("\\", "/")
            json_path = os.path.join(dir_path, json_file)
            
            # Load into PyMOL
            cmd.load(struct_path, "target_model")
            cmd.show_as("cartoon", "target_model")
            cmd.zoom("target_model")
            
            # Extract Metrics
            self.pae_data, self.plddt_data = self.parse_alphafold_json(json_path)
            
            # 1. Render PAE Plot (if available)
            if self.pae_data is not None:
                N = self.pae_data.shape[0]
                # Extent ensures axes directly match 1-indexed residue IDs
                cax = self.ax_pae.imshow(self.pae_data, cmap='bwr_r', vmin=0, vmax=30, extent=[0.5, N + 0.5, N + 0.5, 0.5])
                self.colorbar = self.figure.colorbar(cax, ax=self.ax_pae, label="Expected Position Error (Å)")
            else:
                print("Warning: Missing or unreadable PAE matrix inside selected JSON.")
                
            # 2. Render pLDDT Plot (if available)
            if self.plddt_data is not None:
                residue_indices = np.arange(1, len(self.plddt_data) + 1)
                self.ax_plddt.plot(residue_indices, self.plddt_data, color='#1f77b4', linewidth=2)
                # Draw cutoff lines indicating standard AlphaFold confidence boundaries
                self.ax_plddt.axhline(90, color='darkblue', linestyle=':', alpha=0.5, label='Very High (>90)')
                self.ax_plddt.axhline(70, color='lightblue', linestyle=':', alpha=0.5, label='Confident (>70)')
                self.ax_plddt.axhline(50, color='orange', linestyle=':', alpha=0.5, label='Low (>50)')
            else:
                print("Warning: Missing or unreadable pLDDT metrics inside selected JSON.")

            self.figure.tight_layout()
            self.canvas.draw()
        else:
            QtWidgets.QMessageBox.warning(self, "Files Missing", "Could not locate matching structures (.pdb/.cif) and metric registries (.json).")

    def handle_mode_toggle(self):
        """Applies iconic AlphaFold rainbow color standards utilizing structural B-Factors."""
        # AlphaFold maps overall accuracy metrics directly to the atom B-Factor indices
        cmd.color("red", "target_model and b < 50")
        cmd.color("orange", "target_model and b >= 50 and b < 70")
        cmd.color("lightblue", "target_model and b >= 70 and b < 90")
        cmd.color("darkblue", "target_model and b >= 90")
        print("Model standard alpha-color scale applied via B-Factors.")

    def reset_view(self):
        """Cleans selections, masks sidechains, and focuses back to whole-molecule view."""
        cmd.delete("click_highlight")
        cmd.hide("sticks")
        cmd.show("cartoon", "target_model")
        cmd.zoom("all")
        print("PyMOL frame and layouts reset.")

    def on_canvas_click(self, event):
        """Routes viewport clicks dynamically based on which plot environment is selected."""
        if event.inaxes is None:
            return
        if event.xdata is None or event.ydata is None:
            return

        # Clear out any prior interactive selection highlights
        cmd.delete("click_highlight")

        # --- CASE A: User interacted with the PAE Heatmap ---
        if event.inaxes == self.ax_pae:
            if self.pae_data is None: return
            res1 = int(round(event.xdata))
            res2 = int(round(event.ydata))
            
            print(f"PAE Heatmap Hit: Analyzing Inter-domain error between Residue {res1} and {res2}")
            
            # Select both residue targets
            cmd.select("click_highlight", f"target_model and (resi {res1} or resi {res2})")
            cmd.show("sticks", "click_highlight")
            cmd.color("magenta", "click_highlight")
            cmd.zoom("click_highlight", buffer=6.0)

        # --- CASE B: User interacted with the pLDDT Graph ---
        elif event.inaxes == self.ax_plddt:
            if self.plddt_data is None: return
            res = int(round(event.xdata))
            score = event.ydata
            
            print(f"pLDDT Trace Hit: Isolating position {res} (Local confidence score: {score:.1f})")
            
            # Select single target position
            cmd.select("click_highlight", f"target_model and resi {res}")
            cmd.show("sticks", "click_highlight")
            cmd.color("magenta", "click_highlight")
            cmd.zoom("click_highlight", buffer=6.0)

def start_alpha_viewer():
    global alpha_viewer_instance
    if alpha_viewer_instance is None:
        alpha_viewer_instance = PyMOLAlphaFoldViewer()
        
    alpha_viewer_instance.show()
    alpha_viewer_instance.raise_()

if __name__ == '__main__':
    start_alpha_viewer()