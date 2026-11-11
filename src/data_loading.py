# Loading and merging of the raw PVS dataset files.

import pandas as pd

from src.config import DATA_RAW, RECORDING_TO_CAR, RECORDING_TO_SCENARIO

# Raw label column -> class name used as target
SURFACE_NAMES = {
    "asphalt_road": "asphalt",
    "cobblestone_road": "cobblestone",
    "dirt_road": "dirt",
}

# Prefixes of the phisical sensor columns (accelerometer, gyroscope, magnetometer, temperature)
SENSOR_PREFIXES = ("acc_", "gyro_", "mag_", "temp_")

# Columns of the merged file that must never reach the models: GPS coordinates identify
# the place (hance the road) and would be a shortcut
_DROPPED_COLUMNS = ["timestamp_gps", "latitude", "longitude"]

def sensor_columns(df: pd.DataFrame) -> list[str]:
    # Return the names of the physical sensor columns of "df" (acc, gyro, mag, temp)
    return [c for c in df.columns if c.startswith(SENSOR_PREFIXES)]

def load_recording(recording_id: int, side: str = "left") -> pd.DataFrame:
    # Load one PVS recording as a single DataFrame (one row per 100 Hz sample)
    if side not in ("left", "right"):
        raise ValueError(f"side must be 'left' or 'right' got {side!r}")

    folder = DATA_RAW / f"PVS{recording_id}"
    sensors = pd.read_csv(folder / f"dataset_gps_mpu_{side}.csv")
    labels = pd.read_csv(folder / "dataset_labels.csv")

    # Labels carry no timestamp: they are aligned with the sensors by row position
    if len(sensors) != len(labels):
        raise ValueError(
            f"PVS{recording_id}: {len(sensors)} sensor rows but {len(labels)} label rows"
        )

    df = sensors.drop(columns=_DROPPED_COLUMNS).rename(columns={"speed": "speed_mps"})

    # Target: the single active surface column; NaN if none or several are active.
    # Ambiguos rows are kept (not dropped) so the 100 Hz time series has no gaps
    surface = labels[list(SURFACE_NAMES)]
    df["target"] = surface.idmax(axis=1).map(SURFACE_NAMES).where(surface.sum(axis=1) == 1)

    # Speed bumps are kept as a flag
    df["speed_bump"] = labels["no_speed_bump"] == 0

    # Identifiers: used only to build validation gruops, never as features
    df["recording_id"] = recording_id
    df["car_id"] = RECORDING_TO_CAR[recording_id]
    df["scenario_id"] = RECORDING_TO_SCENARIO[recording_id]
    df["side"] = side

    return df

def load_all(side: str = "left", recordings=range(1,10)) -> pd.DataFrame:

    # Load several recordings and stack them in a single DataFrame
    return pd.concat([load_recording(r, side) for r in recordings], ignore_index=True)


