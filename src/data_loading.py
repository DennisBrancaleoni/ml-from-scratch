# Loading of the raw PVS recordings into one DataFrame
import pandas as pd

from src.config import DATA_RAW, RECORDING_TO_CAR, RECORDING_TO_SCENARIO

# Raw label column -> class name used as target
SURFACE_NAMES = {
    "asphalt_road": "asphalt",
    "cobblestone_road": "cobblestone",
    "dirt_road": "dirt",
}

# GPS coordinates identify the place (hence the road): they would be a shortcut
_DROPPED_COLUMNS = ["timestamp_gps", "latitude", "longitude"]


def load_recording(recording_id: int, side: str = "left") -> pd.DataFrame:
    # Load one recording: sensors, GPS speed, target and identifiers (one row per sample)
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right', got {side!r}")

    folder = DATA_RAW / f"PVS{recording_id}"
    sensors = pd.read_csv(folder / f"dataset_gps_mpu_{side}.csv")
    labels = pd.read_csv(folder / "dataset_labels.csv")

    # Labels have no timestamp: they are aligned with the sensors by row position
    if len(sensors) != len(labels):
        raise ValueError(f"PVS{recording_id}: sensors and labels have different lengths")

    df = sensors.drop(columns=_DROPPED_COLUMNS).rename(columns={"speed": "speed_mps"})

    # Target: name of the surface whose one-hot column is 1.
    # In PVS2 one sample has two active labels: idxmax keeps the first
    surface = labels[list(SURFACE_NAMES)]
    df["target"] = surface.idxmax(axis=1).map(SURFACE_NAMES)

    # Speed bumps are kept as a flag
    df["speed_bump"] = labels["no_speed_bump"] == 0

    # Identifiers: only to build validation groups, never features
    df["recording_id"] = recording_id
    df["car_id"] = RECORDING_TO_CAR[recording_id]
    df["scenario_id"] = RECORDING_TO_SCENARIO[recording_id]
    df["side"] = side
    return df

# Load the 9 recordings and stack them in one DataFrame 
def load_all(side: str = "left") -> pd.DataFrame:
    return pd.concat([load_recording(r, side) for r in range(1, 10)], ignore_index=True)