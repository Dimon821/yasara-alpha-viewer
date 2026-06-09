import os
import json
import numpy as np

# Import YASARA module (must be run within YASARA or with yasara module in PYTHONPATH)
import yasara_main

# Dynamically handle PyQt/PySide depending on what environment YASARA is using
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

class YasaraAlphaFoldViewer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(YasaraAlphaFoldViewer, self).__init__(parent)
        self.setWindowTitle("YASARA AlphaFold PAE & pLDDT Viewer")
        self.resize(800, 700)
        
        self.current_dataset_dir = None
        self.pae_data = None
        
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
        
        # Matplotlib Canvas Setup
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)
        
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Predicted Aligned Error (PAE)")
        self.ax.set_xlabel("Scored residue")
        self.ax.set_ylabel("Aligned residue")
        
        # --- Callbacks & Connections ---
        self.btn1.clicked.connect(self.handle_mode_toggle)
        self.btn2.clicked.connect(self.reset_view)
        self.btn3.clicked.connect(self.handle_change_dataset)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def select_dataset_dialog(self):
        """Opens a folder picker to select the dataset directory."""
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select AlphaFold Output Folder")
        return dir_path

    def parse_alphafold_json(self, json_path):
        """Safely parses PAE data from standard AlphaFold or ColabFold JSON formats."""
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            data = data[0]
            
        pae = data.get('pae') or data.get('predicted_aligned_error') or data.get('distance')
        
        if pae is not None:
            return np.array(pae)
        return None

    def reset_model(self):
        """Clears the YASARA workspace and resets the Matplotlib plot."""
        yasara_main.run("Clear")
        self.ax.clear()
        self.ax.set_title("Predicted Aligned Error (PAE)")
        self.canvas.draw()
        self.pae_data = None

    def handle_change_dataset(self):
        """Handles loading a new PDB/CIF and its corresponding PAE JSON into YASARA."""
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
        json_file = next((f for f in files if f.endswith(".json") and ("pae" in f.lower() or "scores" in f.lower() or "rank" in f.lower())), None)
        
        if struct_file and json_file:
            struct_path = os.path.join(dir_path, struct_file).replace("\\", "/")
            json_path = os.path.join(dir_path, json_file)
            
            # Load structure into YASARA and set visual style
            yasara_main.run(f'LoadPDB "{struct_path}"')
            yasara_main.run('Style Ribbon')
            yasara_main.run('CenterAll')
            
            # Parse and plot the PAE matrix
            self.pae_data = self.parse_alphafold_json(json_path)
            if self.pae_data is not None:
                cax = self.ax.imshow(self.pae_data, cmap='bwr', vmin=0, vmax=30)
                self.figure.colorbar(cax, ax=self.ax, label="Expected Position Error (Å)")
                self.canvas.draw()
            else:
                print("Warning: Could not find a recognizable PAE array in the provided JSON.")
        else:
            QtWidgets.QMessageBox.warning(self, "Files Missing", "Could not locate both a structure file (.pdb/.cif) and a PAE JSON file in the selected directory.")

    def handle_mode_toggle(self):
        """Colors the model by pLDDT using YASARA's B-factor coloring."""
        # AlphaFold puts pLDDT in the B-factor column. YASARA can color by B-factor directly.
        yasara_main.run("ColorRes all, BFactor")
        print("Model colored by pLDDT (B-factor).")

    def reset_view(self):
        """Centers the view on the whole molecule and hides sidechains."""
        yasara_main.run("HideAtom Sidechain")
        yasara_main.run("CenterAll")
        yasara_main.run("ZoomAll")
        print("View reset.")

    def on_canvas_click(self, event):
        """Translates a click on the PAE heatmap into a YASARA selection & zoom."""
        if event.inaxes != self.ax or self.pae_data is None:
            return
        if event.xdata is None or event.ydata is None:
            return
            
        res1 = int(round(event.xdata)) + 1
        res2 = int(round(event.ydata)) + 1
        
        # Show sidechains, color them, and zoom in YASARA
        yasara_main.run(f"ShowAtom Res {res1} {res2} and Sidechain")
        yasara_main.run(f"ColorRes {res1} {res2}, Magenta")
        yasara_main.run(f"ZoomRes {res1} {res2}")
        
        print(f"Highlighted cross-residue interaction in YASARA: Residue {res1} and Residue {res2}")

def start_alpha_viewer():
    global alpha_viewer_instance
    if alpha_viewer_instance is None:
        alpha_viewer_instance = YasaraAlphaFoldViewer()
        
    alpha_viewer_instance.show()
    alpha_viewer_instance.raise_()

# If running directly inside YASARA's python console
if __name__ == '__main__':
    start_alpha_viewer()