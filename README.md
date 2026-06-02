# YASARA AlphaFold Viewer

An interactive, dual-panel analysis dashboard that bridges 1D/2D AlphaFold structural prediction metrics with 3D molecular viewports. This tool synchronizes a high-contrast Matplotlib control interface with YASARA to dynamically render structural validation metrics on demand.

---

## Key Features

* **Dual-Metric Dashboard:** View both 2D Predicted Aligned Error (PAE) matrices and 1D pLDDT confidence profiles simultaneously.
* **Dynamic PAE Structure Mapping:** Click anywhere on the 2D PAE matrix chart to set a local "focus residue." The tool automatically queries the structural alignments and re-colors the 3D YASARA viewport based on errors relative to that selection.
* **Native pLDDT Color Schemes:** Instantly toggle structural colorations matching standard AlphaFold confidence bands:
    * **Blue** (>= 90 pLDDT): Very high confidence
    * **Cyan** (70 to 90 pLDDT): Confident
    * **Yellow** (50 to 70 pLDDT): Low confidence
    * **Red** (< 50 pLDDT): Very low confidence / disordered
* **Live Dataset Swapping:** Change files on the fly. Clicking the directory selection button invokes a native Windows folder picker to reload target protein models without terminating the application runtime thread.

---

## System Prerequisites

To use this visualization suite, your local environment requires:

1. Windows OS (with administrative rights for cross-process communication sockets).
2. Python 3.10+
3. An active installation of YASARA (with the python interface plugins enabled).

---

## Installation & Setup

### 1. Clone the Workspace
```bash
git clone [https://github.com/YOUR_USERNAME/yasara-alpha-viewer.git](https://github.com/YOUR_USERNAME/yasara-alpha-viewer.git)
cd yasara-alpha-viewer