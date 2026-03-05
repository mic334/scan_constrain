# scan_constrain

`scan_constrain` is a small utility designed to help when a **Gaussian scan calculation fails** during a potential energy scan.

Instead of rerunning the entire scan, this tool allows you to **generate new Gaussian input files where selected coordinates are constrained**. This makes it easier to recover problematic points or recompute parts of the scan in a more stable way.

The script automates the creation of multiple Gaussian jobs with **fixed geometric constraints** (e.g., bonds, angles, or dihedrals).

---

## Motivation

Potential energy scans in Gaussian sometimes fail due to:
- SCF convergence problems
- geometry optimization failures
- problematic intermediate geometries

When this happens, restarting the entire scan is inefficient.

`scan_constrain` helps by:
- extracting geometries from a scan
- applying **constraints to selected coordinates**
- generating **separate Gaussian input files** for each point

This allows you to recompute specific configurations with better control.

---

## Features

- Generate multiple Gaussian input files from a scan
- Apply geometric constraints to selected coordinates
- Recover problematic scan points
- Simple command-line workflow
- Easily integrable in HPC job pipelines

---

## Requirements

- Python 3.x
- Gaussian (g16 / g09 or compatible)

Optional:
- Linux/macOS environment recommended
- HPC scheduler (SLURM/PBS) for batch execution

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mic334/scan_constrain.git
cd scan_constrain
