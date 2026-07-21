import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy import distance

from pycontrails import Flight

from cane.models.aircraft_performance import get_wing_span


def df_to_flight(df: pd.DataFrame, bada_3_path: str) -> Flight:
    mass0 = df.aircraft_mass.iloc[0]
    flight_id = df.flight_id.iloc[0]
    typecode = df.typecode.iloc[0]

    flight = Flight(
        time=df.timestamp,

        latitude=df.latitude,
        longitude=df.longitude,
        altitude_ft=df.altitude_ft,

        data=df,

        attrs={
            "flight_id": flight_id,
            "aircraft_type": typecode,
            "takeoff_mass": mass0,
            "wingspan": get_wing_span(typecode, bada_3_path)
        },
        drop_duplicated_times=False
    )
    return flight


def get_time_bounds(df1: pd.DataFrame, df2: pd.DataFrame, timedelta: pd.Timedelta = None, round: str = "h") -> tuple:
    """
        Determine the time bounds (min and max) of two dfs with a timestamp column.
        :param df1: pd.DataFrame
        :param df2: pd.DataFrame
        :param timedelta: pd.Timedelta
        :param round: round to nearest hour ("h"), ...
        :return: time bounds (min, max)
    """
    if "timestamp" not in df1.columns:
        raise ValueError("timestamp column not found in df1")
    if "timestamp" not in df2.columns:
        raise ValueError("timestamp column not found in df2")
    t_min = min(df1.timestamp.min(), df2.timestamp.min())
    t_max = max(df1.timestamp.max(), df2.timestamp.max())
    if timedelta is not None:
        t_max += timedelta
    return str(t_min.floor(round)), str(t_max.ceil(round))


def get_lat_lon_bounds(df1: pd.DataFrame, df2: pd.DataFrame):
    """
        Get the coordinates bounds (min and max) of two dfs with latitude and longitude columns.
        :param df1: pd.DataFrame
        :param df2: pd.DataFrame
        :return: coordinates bounds (min, max)
    """
    if "latitude" not in df1.columns or "longitude" not in df1.columns:
        raise ValueError("latitude and longitude columns are required in df1")
    if "latitude" not in df2.columns or "longitude" not in df2.columns:
        raise ValueError("latitude and longitude columns are required in df2")
    lat_bounds = [
        np.floor(min(df1["latitude"].min(), df2["latitude"].min())),
        np.ceil(max(df1["latitude"].max(), df2["latitude"].max()))
    ]
    lon_bounds = [
        np.floor(min(df1["longitude"].min(), df2["longitude"].min())),
        np.ceil(max(df1["longitude"].max(), df2["longitude"].max()))
    ]
    return lat_bounds, lon_bounds


def df_diff(org_df, opt_df, on="flight_id", keep_originals=False):
    assert np.all(org_df.columns == opt_df.columns)
    merged = org_df.merge(opt_df, on=on, suffixes=("_filed", "_optimised"))
    cols = []
    out = None
    if type(on) is str:
        cols = [c for c in org_df.columns if c != on]
        out = merged if keep_originals else pd.DataFrame({on: merged[on]})  # TODO
    elif type(on) is list:
        cols = [c for c in org_df.columns if c not in on]
        out = merged if keep_originals else pd.DataFrame({on: merged[on]})  # TODO
    for c in cols:
        diff = merged[f"{c}_optimised"] - merged[f"{c}_filed"]
        out[f"{c}_diff"] = diff
        out[f"{c}_reldiff"] = diff / merged[f"{c}_filed"]
    return out


def flatten_list(my_list):
    return [item for sublist in my_list for item in sublist]


def mask_by_validity_range(fleet, columns, bounds=[200, 350], new_value=0):
    """
    Set selected 'columns' to 0 for all rows, which are outside (< or >) the bounds.
    :param fleet: pycontrails.Fleet object
    :param columns: list of column names
    :param bounds: array of lower and upper bounds in [hPa]. Both included.
    :param new_value: new substitution value, e.g. 0 or NaN
    """
    mask = (fleet["air_pressure"] >= bounds[0] * 100) & (fleet["air_pressure"] <= bounds[1] * 100)
    for col in columns:
        new_col = np.where(mask, fleet[col], new_value)
        fleet.update({col: new_col})
        print(f"Bounds of {bounds} in place for {col}")


def mask_by_marker(fleet, columns, new_value=0):
    """
    Set selected columns to 0 for all rows where 'is_excluded' is True.
    :param fleet:
    :param columns:
    :param new_value:
    """
    mask = fleet["is_excluded"] == True
    for col in columns:
        new_col = np.where(mask, new_value, fleet[col])
        fleet.update({col: new_col})
        print(f"Marked rows filtered out for {col}")


def set_font_size(font_size: int = 14):
    plt.rcParams.update({
        "axes.titlesize": font_size,
        "axes.labelsize": font_size,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "legend.fontsize": font_size
    })

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


def haul_type_by_distance_ectl(df):
    df["haul_type"] = np.where(df.flown_distance > 4000, "Long", "Medium")
    df["haul_type"] = np.where(df.flown_distance < 1500, "Short", df["haul_type"])
    return df

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