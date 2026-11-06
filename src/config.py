"""Project constants and paths.

All paths are relative to the repository root (computed from this file), so the code
works on any machine and from the notebook in `notebooks/`.
"""

from pathlib import Path

# --- Paths --------------------------------------------------------------------
# Repository root: this file lives in <root>/src/config.py
ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"              # PVS dataset downloaded from Kaggle
DATA_PROCESSED = ROOT / "data" / "processed"  # table of windows (parquet)
FIGURES = ROOT / "figures"                    # plots saved by the notebook

# --- Reproducibility ----------------------------------------------------------
RANDOM_STATE = 42  # single seed for every random component

# --- Signal parameters --------------------------------------------------------
SAMPLING_RATE_HZ = 100  # sampling rate of the MPU-9250 sensors
