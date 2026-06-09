import os
import json
import time
import numpy as np
from pymol import cmd
import requests
import concurrent.futures

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

# --- Asynchronous InterPro Scan Engines ---
def get_interpro_domains(sequence: str, chain_id: str, email: str = "your_email@example.com"):
    if not sequence or len(sequence.strip()) < 5:
        return chain_id, []

    submit_url = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/run"
    status_base_url = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/status/"
    result_base_url = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5/result/"

    payload = {
        "email": email,
        "title": f"AF3_Chain_{chain_id}_Domain_Scan",
        "sequence": sequence.strip(),
        "goterms": "false",
        "pathways": "false",
    }

    try:
        response = requests.post(submit_url, data=payload, timeout=30)
        if response.status_code != 200: return chain_id, []
        job_id = response.text.strip()
        print(f"[Worker] Chain {chain_id} running... Job ID: {job_id}")

        while True:
            time.sleep(6)
            status = requests.get(f"{status_base_url}{job_id}", timeout=15).text.strip()
            if status == "FINISHED": break
            if status in ["FAILED", "ERROR"]: return chain_id, []

        result_resp = requests.get(f"{result_base_url}{job_id}/json", timeout=20)
        if result_resp.status_code != 200: return chain_id, []

        data = result_resp.json()
        domains = []
        for match in data.get("results", []):
            signature = match.get("signature", {})
            interpro_entry = signature.get("entry", {})
            if interpro_entry and interpro_entry.get("type") == "Domain":
                for loc in match.get("locations", []):
                    domains.append({
                        "name": interpro_entry.get("name"),
                        "id": interpro_entry.get("ac"),
                        "start": loc.get("start"),
                        "end": loc.get("end")
                    })
        return chain_id, domains
    except Exception as e:
        print(f"[Worker] Chain {chain_id} network exception: {e}")
        return chain_id, []

class DomainFetchWorker(QtCore.QThread):
    finished_signal = QtCore.Signal(dict)
    log_signal = QtCore.Signal(str)

    def __init__(self, chain_sequences):
        super().__init__()
        self.chain_sequences = chain_sequences

    def run(self):
        self.log_signal.emit("Launching background annotation workers...")
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.chain_sequences)+1) as executor:
            future_to_chain = {
                executor.submit(get_interpro_domains, seq, chain): chain 
                for chain, seq in self.chain_sequences.items()
            }
            for future in concurrent.futures.as_completed(future_to_chain):
                chain = future_to_chain[future]
                try:
                    chain_id, domains = future.result()
                    results[chain_id] = domains
                    self.log_signal.emit(f"✓ Chain {chain_id} annotation completed.")
                except Exception as exc:
                    self.log_signal.emit(f"✗ Chain {chain} thread error: {exc}")
                    results[chain] = []
        self.finished_signal.emit(results)


# --- Dashboard Window Layout ---
class AlphaFoldViewer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AlphaFoldViewer, self).__init__(parent)
        self.setWindowTitle("AlphaFold 3 Multimer Interactive Workspace")
        self.resize(1200, 780)
        
        self.current_dataset_dir = None
        self.pae_data = None
        self.plddt_data = None
        self.chain_info = []
        self.current_model_name = "af_model"
        self.colorbar = None
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # --- Native Folder Selector GUI Bar ---
        path_layout = QtWidgets.QHBoxLayout()
        self.path_input = QtWidgets.QLineEdit()
        self.path_input.setPlaceholderText("No Directory Selected...")
        self.path_input.setReadOnly(True)  # Protect against typos
        self.btn_browse = QtWidgets.QPushButton("Browse Folders...")
        self.btn_load = QtWidgets.QPushButton("Load Analysis Dashboard")
        self.btn_load.setEnabled(False)
        
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.btn_browse)
        path_layout.addWidget(self.btn_load)
        main_layout.addLayout(path_layout)
        
        # Control Row
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn1 = QtWidgets.QPushButton("Color Complex by pLDDT")
        self.btn2 = QtWidgets.QPushButton("Reset Viewport")
        self.lbl_status = QtWidgets.QLabel("Status: Workspace Idle")
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)
        btn_layout.addWidget(self.lbl_status)
        main_layout.addLayout(btn_layout)
        
        # Matplotlib Area
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.toolbar)
        
        self.ax_pae = self.figure.add_subplot(121)
        self.ax_plddt = self.figure.add_subplot(122)
        self.setup_blank_plots()
        
        # Button Bindings
        self.btn_browse.clicked.connect(self.handle_browse_directory)
        self.btn_load.clicked.connect(self.handle_change_dataset)
        self.btn1.clicked.connect(self.handle_mode_toggle)
        self.btn2.clicked.connect(self.reset_model)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def setup_blank_plots(self):
        self.ax_pae.clear()
        self.ax_pae.set_title("Predicted Aligned Error (PAE)")
        self.ax_pae.set_xlabel("Scored residue")
        self.ax_pae.set_ylabel("Aligned residue")
        
        self.ax_plddt.clear()
        self.ax_plddt.set_title("10-Residue Smoothed pLDDT Track Profile")
        self.ax_plddt.set_xlabel("Complex Absolute Residue Position")
        self.ax_plddt.set_ylabel("pLDDT (10-Residue Centered MA)")
        self.ax_plddt.set_ylim(0, 105)
        self.ax_plddt.grid(True, linestyle='--', alpha=0.4)

    def handle_browse_directory(self):
        """Launches a native OS directory select interface window."""
        starting_dir = os.path.expanduser("~/Downloads")
        selected_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select AlphaFold Output Directory", starting_dir
        )
        if selected_dir:
            self.path_input.setText(selected_dir)
            self.current_dataset_dir = selected_dir
            self.btn_load.setEnabled(True)

    def extract_chains_from_pymol(self):
        self.chain_info = []
        chain_sequences = {}
        stored_data = []
        
        cmd.iterate(f"{self.current_model_name} and name CA", 
                    "stored_data.append((chain, int(resi), resn))", 
                    space={'stored_data': stored_data})
        
        if not stored_data: return {}
            
        aa_map = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H','ILE':'I',
                  'LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
                  
        current_chain = None
        start_idx = 0
        
        for i, (chain, resi, resn) in enumerate(stored_data):
            if chain != current_chain:
                if current_chain is not None:
                    self.chain_info.append((current_chain, start_idx, i - 1))
                current_chain = chain
                start_idx = i
                chain_sequences[chain] = ""
            chain_sequences[chain] += aa_map.get(resn, 'X')
            
        self.chain_info.append((current_chain, start_idx, len(stored_data) - 1))
        return chain_sequences

    def calculate_moving_average(self, data, window=10):
        if len(data) < window: return data
        weights = np.ones(window) / window
        return np.convolve(data, weights, mode='same')

    def handle_change_dataset(self):
        if not self.current_dataset_dir: return
        self.reset_model()
        
        struct_path, json_path = None, None
        for root, _, files in os.walk(self.current_dataset_dir):
            if "templates" in root or "msas" in root: continue
            files.sort()
            for f in files:
                if (f.endswith(".cif") or f.endswith(".pdb")) and "template" not in f.lower() and not struct_path:
                    struct_path = os.path.join(root, f)
                if f.endswith(".json") and "full_data" in f and not json_path:
                    json_path = os.path.join(root, f)

        if struct_path and json_path:
            self.lbl_status.setText("Status: Reading datasets...")
            cmd.load(struct_path, self.current_model_name)
            cmd.show_as("cartoon", self.current_model_name)
            cmd.orient(self.current_model_name)
            
            chain_sequences = self.extract_chains_from_pymol()
            
            # Extract exactly ONE pLDDT value per residue from Alpha Carbons
            ca_plddt = []
            cmd.iterate(f"{self.current_model_name} and name CA", "ca_plddt.append(b)", space={'ca_plddt': ca_plddt})
            self.plddt_data = np.array(ca_plddt)
            
            if self.plddt_data is not None and np.max(self.plddt_data) <= 1.0:
                self.plddt_data *= 100.0

            with open(json_path, 'r') as f:
                raw_data = json.load(f)
            if isinstance(raw_data, list): raw_data = raw_data[0]
            pae = raw_data.get('pae') or raw_data.get('predicted_aligned_error')
            self.pae_data = np.array(pae) if pae is not None else None
            
            # --- Render PAE Heatmap + Split Grid bars ---
            if self.pae_data is not None:
                if len(self.pae_data.shape) == 1:
                    n = int(np.sqrt(self.pae_data.shape[0]))
                    self.pae_data = self.pae_data.reshape((n, n))
                
                cax = self.ax_pae.imshow(self.pae_data, cmap='bwr', vmin=0, vmax=30)
                self.colorbar = self.figure.colorbar(cax, ax=self.ax_pae, label="Expected Error (Å)", orientation='horizontal', pad=0.12)
                
                for i in range(len(self.chain_info) - 1):
                    end_idx = self.chain_info[i][2]
                    self.ax_pae.axvline(x=end_idx, color='black', linestyle='--', linewidth=1.5)
                    self.ax_pae.axhline(y=end_idx, color='black', linestyle='--', linewidth=1.5)

            # --- Render Smoothed 10-Residue pLDDT Plot ---
            total_residues = len(self.plddt_data) if self.plddt_data is not None else 0
            if self.plddt_data is not None and total_residues > 0:
                smoothed_plddt = self.calculate_moving_average(self.plddt_data, window=10)
                abs_positions = np.arange(1, total_residues + 1)
                
                colors_pool = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                for idx, (chain_id, start, end) in enumerate(self.chain_info):
                    c_color = colors_pool[idx % len(colors_pool)]
                    self.ax_plddt.plot(abs_positions[start:end+1], smoothed_plddt[start:end+1], 
                                       color=c_color, linewidth=2.5, label=f"Chain {chain_id}")
                    
                    if idx < len(self.chain_info) - 1:
                        self.ax_plddt.axvline(x=end+1, color='grey', linestyle=':', linewidth=1.2)
                
                self.ax_plddt.set_xlim(1, total_residues)
                self.ax_plddt.legend(loc='lower left', fontsize='small')

            self.canvas.draw()
            self.handle_mode_toggle()
            
            if chain_sequences:
                self.lbl_status.setText("Status: Executing parallel InterPro mappings...")
                self.worker = DomainFetchWorker(chain_sequences)
                self.worker.log_signal.connect(lambda text: print(text))
                self.worker.finished_signal.connect(self.process_async_annotations)
                self.worker.start()
        else:
            self.lbl_status.setText("Status: Parsing scan exception error.")

    def process_async_annotations(self, annotation_results):
        print("\n--- Mapping Domain Annotations ---")
        box_colors = ['gold', 'orchid', 'turquoise', 'lightcoral', 'yellowgreen']
        color_idx = 0
        track_y = 12 
        
        for chain_id, domains in annotation_results.items():
            boundary = next((info for info in self.chain_info if info[0] == chain_id), None)
            if not boundary or not domains: continue
            offset = boundary[1]
            
            for dom in domains:
                abs_start = offset + dom['start']
                abs_end = offset + dom['end']
                
                box_color = box_colors[color_idx % len(box_colors)]
                color_idx += 1
                
                # Overlay background span indicator blocks on line profile
                self.ax_plddt.axvspan(abs_start, abs_end, ymin=0.04, ymax=0.12, color=box_color, alpha=0.35)
                self.ax_plddt.text((abs_start + abs_end)/2, track_y, dom['name'], 
                                   fontsize=7.5, weight='bold', ha='center', va='center',
                                   bbox=dict(boxstyle='round,pad=0.25', facecolor=box_color, alpha=0.85))
                
                safe_name = f"dom_{chain_id}_{dom['id']}"
                cmd.select(safe_name, f"({self.current_model_name} and chain {chain_id} and resi {dom['start']}-{dom['end']})")
                cmd.color("lightpink", safe_name)
            
            track_y += 14

        self.canvas.draw()
        self.lbl_status.setText("Status: Computations Complete")

    def reset_model(self):
        cmd.delete("all")
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None
        self.setup_blank_plots()
        self.canvas.draw()
        self.pae_data, self.plddt_data = None, None
        self.lbl_status.setText("Status: System Reset")

    def handle_mode_toggle(self):
        stored_b = []
        cmd.iterate(self.current_model_name, "stored_b.append(b)", space={'stored_b': stored_b})
        max_b = max(stored_b) if stored_b else 100
        min_lim, max_lim = (50, 90) if max_b > 1.0 else (0.5, 0.9)
        cmd.spectrum("b", "red_yellow_green_cyan_blue", self.current_model_name, minimum=min_lim, maximum=max_lim)

    def on_canvas_click(self, event):
        if event.xdata is None or event.ydata is None or not self.chain_info: return
        abs_res = int(round(event.xdata))
        
        def find_chain_coords(abs_idx):
            for chain_id, start, end in self.chain_info:
                if start <= abs_idx - 1 <= end:
                    return chain_id, (abs_idx - 1 - start) + 1
            return None, None

        if event.inaxes == self.ax_pae:
            ch1, r1 = find_chain_coords(int(round(event.xdata)))
            ch2, r2 = find_chain_coords(int(round(event.ydata)))
            if ch1 and ch2:
                query = f"({self.current_model_name} and chain {ch1} and resi {r1}) or ({self.current_model_name} and chain {ch2} and resi {r2})"
            else: return
        elif event.inaxes == self.ax_plddt:
            ch, r = find_chain_coords(abs_res)
            if ch: query = f"{self.current_model_name} and chain {ch} and resi {r}"
            else: return
        else: return
            
        sele_name = "dashboard_interaction"
        cmd.select(sele_name, query)
        cmd.show("sticks", sele_name)
        cmd.zoom(sele_name, buffer=6.0)

def start_alpha_viewer():
    global alpha_viewer_instance
    if alpha_viewer_instance is None:
        try:
            from pymol.qt import get_main_window
            parent = get_main_window()
        except: parent = None
        alpha_viewer_instance = AlphaFoldViewer(parent=parent)
    alpha_viewer_instance.show()
    alpha_viewer_instance.raise_()

cmd.extend("start_alpha_viewer", start_alpha_viewer)
start_alpha_viewer()