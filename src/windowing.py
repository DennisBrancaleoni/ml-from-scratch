# Signal segmentation into windows and window labelling 
import numpy as np
import pandas as pd

from src.config import (
    CLASS_ORDER, MIN_SPEED_MPS, PURITY_MIN, SAMPLING_RATE_HZ, WINDOW_OVERLAP, WINDOW_SECONDS,
)

def window_recording(rec: pd.DataFrame, window_size: int, step: int) -> pd.DataFrame: 
    
    # Describe the windows of 1 recording (start/end positinos, label, purity, speed, bump)
    rec = rec.reset_index(drop=True)

    # Number of samples of each class inside every window that ends at each row
    # Counts are exact integers, so 160 / 200 = 0.8 without rounding errors
    onehot = pd.get_dummies(rec["target"]).reindex(columns=CLASS_ORDER, fill_value=0)
    counts = onehot.astype(float).rolling(window_size).sum()

    # Index of the last sample of each window: the first window ends at row window_size - 1
    ends = np.arange(window_size - 1, len(rec), step)

    fractions = counts.iloc[ends] / window_size
    win = pd.DataFrame({"start": ends - window_size + 1, "end": ends + 1}) # end is exlusive
    win["target"] = fractions.idxmax(axis=1).to_numpy()
    win["purity"] = fractions.max(axis=1).to_numpy()
    win["speed_mean"] = rec["speed_mps"].rolling(window_size).mean().iloc[ends].to_numpy()

    bump = rec["speed_bump"].astype(int).rolling(window_size).max()
    win["has_bump"] = bump.iloc[ends].to_numpy() == 1

    win["recording_id"] = rec["recording_id"].iloc[0]
    win["car_id"] = rec["car_id"].iloc[0]
    win["scenario_id"] = rec["scenario_id"].iloc[0]

    return win

def make_windows(df, window_seconds=WINDOW_SECONDS, overlap=WINDOW_OVERLAP) -> pd.DataFrame:
    
    # Windows of all recordings, one recording at a time (no window crosses two recordings)
    window_size = int(window_seconds * SAMPLING_RATE_HZ)
    step = int(window_size * (1 - overlap))
    parts = [window_recording(rec, window_size, step) for _, rec in df.groupby("recording_id")]

    return pd.concat(parts, ignore_index=True)

def filter_windows(windows, purity_min=PURITY_MIN, min_speed_mps=MIN_SPEED_MPS) -> pd.DataFrame:

    # Keep windows that are pure enouth and not (almost) standing still
    keep = (windows["purity"] >= purity_min) & (windows["speed_mean"] >= min_speed_mps)
    return windows[keep].reset_index(drop=True)