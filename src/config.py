# Project constants and paths.

from pathlib import Path

# Paths
# Repository root: this file lives in <root>/src/config.py
ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"              # PVS dataset downloaded from Kaggle
DATA_PROCESSED = ROOT / "data" / "processed"  # table of windows
FIGURES = ROOT / "figures"                    # plots saved by the notebook

# Reproducibility
RANDOM_STATE = 42  # single seed for every random component

# Signal parameters 
SAMPLING_RATE_HZ = 100  # sampling rate of the MPU-9250 sensors

# Dataset structure
# 3 vehicles x 3 scenarios (routes); every
# vehicle has its own driver, so car effect and driver effect cannot be separated.
# The same 3 routes are driven by all 3 cars.
RECORDING_TO_CAR = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}
RECORDING_TO_SCENARIO = {1: 1, 2: 2, 3: 3, 4: 1, 5: 2, 6: 3, 7: 1, 8: 2, 9: 3}
CAR_NAMES = {1: "Volkswagen Saveiro", 2: "Fiat Bravo", 3: "Fiat Palio"}
