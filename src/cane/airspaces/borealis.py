import pathlib
import json
import numpy as np
import pandas as pd

_path_to_static = pathlib.Path(__file__).parent / "static"

# Variables
borealis_arr = ["EISN", "EGPX", "EGTT", "EKDK", "ESAA", "ENOB", "ENOR", "EVRR", "EETT", "EFIN", "BIRD"]  # no EGGX
borealis_airspaces_piontek2025 = [
    "BIRD", "EGGX", "EISN", "EGPX", "EGTT", "ENOB", "ENOR", "EKDK", "ESAA", "EFIN", "EETT", "EVRR"  # with EGGX, sorted
]
friendly_firs = {
    "BIRD": "Iceland",
    "EGGX": "Shanwick (Ocean)",
    "EISN": "Ireland",
    "EGPX": "Scotland",
    "EGTT": "England",
    "ENOB": "Bodø (Ocean)",
    "ENOR": "Norway",
    "EKDK": "Denmark",
    "ESAA": "Sweden",
    "EFIN": "Finland",
    "EETT": "Estonia",
    "EVRR": "Latvia"
}

# FIRs in EUROCONTROL data often have a 'FIR' or 'UIR' suffix
borealis_arr_ext = np.array([[fir, f'{fir}FIR', f'{fir}UIR'] for fir in borealis_arr]).flatten().tolist()


class Borealis:
    def _load_json(self, path) -> dict:
        with open(path, 'r') as file:
            fc = json.load(file)
        return fc

    def __init__(self):
        self.feature_collection = self._load_json(_path_to_static / "Borealis_airspaces.json")
        self.feature_dict = {f["properties"]["airspace"]: f for f in self.feature_collection["features"]}


def classify_borealis(fps, firs):
    # first merge, then filter down to only rows where the timestamp is inside the interval
    fps_with_fir_entries = (
        pd.merge(fps, firs, on="flight_id", suffixes=(None, "_fir"))
        .loc[lambda d: (d["time_entry"] <= d["timestamp"]) & (d["timestamp"] < d["time_exit"])]
    )

    # merge back with the original fps to have all flights and fill with NaN
    fps = (
        pd.merge(
            fps,
            fps_with_fir_entries[["timestamp"] + list(firs.columns)],
            on=["flight_id", "timestamp"], how="left"
        )
    )
    return fps
