import numpy as np
import pandas as pd
from geopy import distance

def flight_haul_type_by_time(
        df: pd.DataFrame,
        time_col: str = "flight_time",
        classification: str = "IATA") -> pd.DataFrame:
    if classification == "ICAO":
        # short, long, ultra-long
        df["haul_type"] = np.where(df[time_col].dt.total_seconds() > 16 * 3600, "Ultra-long", "Long")
        df["haul_type"] = np.where(df[time_col].dt.total_seconds() < 8 * 3600, "Short", df["haul_type"])
    elif classification == "IATA":
        # short, medium, long, ultra-long
        df["haul_type"] = np.where(df[time_col].dt.total_seconds() > 16 * 3600, "Ultra-long", "Long")
        df["haul_type"] = np.where(df[time_col].dt.total_seconds() < 6 * 3600, "Medium", df["haul_type"])
        df["haul_type"] = np.where(df[time_col].dt.total_seconds() < 3 * 3600, "Short", df["haul_type"])
    return df


def flight_haul_type_by_distance(
        df: pd.DataFrame,
        distance_col: str = "flown_distance") -> pd.DataFrame:
    """
        EUROCONTROL classification
        :param df: pd.DataFrame
        :param distance_col: in [km]
    """
    df["haul_type"] = np.where(df[distance_col] > 4000, "Long", "Medium")
    df["haul_type"] = np.where(df[distance_col] < 500, "Short", df["haul_type"])

    return df

def dist(lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
    """
        Determine segment distance between waypoints in meters
        :param lats:
        :param lons:
        :return: segment distance in [m]
    """
    coords = np.column_stack((lats, lons))
    distances = [
        distance.distance(coords[i], coords[i + 1]).meters
        for i in range(len(coords) - 1)
    ]
    distances.append(np.nan)
    return np.array(distances)


def flown_distance(lats: np.ndarray, lons: np.ndarray) -> float:
    return np.nansum(dist(lats, lons))


#####
##### Optimization type
#####
def cruise_blocks(a):
    # Find where values change
    change_idx = np.flatnonzero(np.diff(a)) + 1

    # Split array into runs
    blocks = np.split(a, change_idx)

    # Keep only blocks with length > 1
    repeat_blocks = [b[0] for b in blocks if len(b) > 1]  # only keep one value per block

    return repeat_blocks


def classify_optimization(cbf, cbo):
    if len(cbf) == len(cbo) == 1 and cbf[0] > cbo[0]:
        return "no_full_climb"
    if len(cbo) > len(cbf):
        if len(cbf) == 0:
            return "no_full_climb"
        if cbo[0] < cbf[0]:
            # if the first cruise phase is lower
            return "late_climb"
        if cbo[-1] < cbf[-1]:
            return "early_descent"
        else:
            return "cruise_dip"
    if len(cbf) == len(cbo):
        if len(cbf) > 0:
            if cbf[0] > cbo[0]:
                return "late_climb"
            if cbf[-1] > cbo[-1]:
                return "early_descent"
            if np.any(cbf > cbo):
                return "cruise_dip"

    return None
