import numpy as np
import pandas as pd
from pycontrails.core import Flight as PyFlight
from pycontrails.ext.bada import BADAFlight

import enum
class APModel(enum.Enum):
    BADA3 = "BADA3"
    BADA4 = "BADA4"
    PollSchumann = "Poll-Schumann"
    OpenAP = "OpenAP"

bada_3_path = "/Users/jsmretschnig/Library/CloudStorage/OneDrive-DelftUniversityofTechnology/Database/BADA 3.16/bada_316_80ddb12010d1cfc55fc7"


def verify_mass(masses: pd.Series):
    duplicates = masses.duplicated().sum()
    if duplicates > 0:
        raise ValueError(f"{duplicates} duplicated aircraft masses found. Zero allowed.")


def verify_fuel_flow(ff: pd.Series):
    nan_count = np.count_nonzero(np.isnan(ff))
    if nan_count > 1:
        raise ValueError(f"Fuel flow is {nan_count}x NaN. Only once allowed (for last waypoint/segment).")

    # from: pycontrails aircraft_performance.py
    # "The max value in the BADA tables is 4.6 kg/s per engine."
    # "Multiplying this by 4 engines and giving a buffer."
    above_limit = np.count_nonzero(ff > 25.0)
    if above_limit > 0:
        raise ValueError(f"Fuel flow is {above_limit}x > 5 kg/s")


def run_bada3_fuel_flow(df: pd.DataFrame):
    fill_isa_temp = True
    fill_zero_wind = True

    mass0 = df.mass.iloc[0]
    flight_id = df.flight_id.iloc[0]
    typecode = df.typecode.iloc[0]
    engine_uid = df.engine_uid.iloc[0]

    flight = PyFlight(
        time=df.timestamp,

        latitude=df.latitude,
        longitude=df.longitude,
        altitude_ft=df.altitude_ft,

        data=df[["true_airspeed"]] if "true_airspeed" in df else None,
        attrs={
            "flight_id": flight_id,
            "aircraft_type": typecode,
            "engine_uid": engine_uid,
            "takeoff_mass": mass0
        },
        drop_duplicated_times=False
    )

    flight.clean_and_resample()

    try:
        bada3_out = BADAFlight(
            # met=met,  # without MET data, i.e. no wind considered
            fill_low_altitude_with_isa_temperature=fill_isa_temp,
            fill_low_altitude_with_zero_wind=fill_zero_wind,
            bada3_path=bada_3_path,
            bada4_path=None,
            bada_priority=3
        ).eval(flight)
        verify_mass(bada3_out.dataframe.aircraft_mass)
        verify_fuel_flow(bada3_out.dataframe.fuel_flow)

        df["BADA3_fuel_flow"] = bada3_out.dataframe.fuel_flow.values
        df["BADA3_fuel_burn"] = bada3_out.dataframe.fuel_burn.values
        df["BADA3_engine_efficiency"] = bada3_out.dataframe.engine_efficiency.values
        df["BADA3_aircraft_mass"] = bada3_out.dataframe.aircraft_mass.values
        df["BADA3_thrust"] = bada3_out.dataframe.thrust.values

        # Save aggregates
        df["BADA3_total_fuel_burn"] = bada3_out.constants["total_fuel_burn"] if bada3_out is not None else np.nan

    except Exception as e:
        print("ERROR", flight_id, e)

    return df

def get_sub_fleet(df: pd.DataFrame, model: APModel) -> pd.DataFrame:
    tmp = df.copy().assign(APModel=model.value)
    tmp = tmp.rename(columns={
        "fuel_flow": "fuel_flow_old",
        "total_fuel_burn": "total_fuel_burn_old",
    })
    return tmp.rename(columns={
        f"{model.value}_aircraft_mass": "aircraft_mass",
        f"{model.value}_fuel_flow": "fuel_flow",
        f"{model.value}_engine_efficiency": "engine_efficiency"
    })


def get_wing_span(typecode: str, bada_3_path: str) -> str:
    try:
        wingspan = (
            BADAFlight(bada3_path=bada_3_path)
            .get_bada(typecode)
            .get_aircraft_params(typecode)
            .wing_span
        )
    except:
        raise ValueError(f"Wing span for {typecode} not found.")
    return wingspan


def get_fleet_attributes(df: pd.DataFrame, bada_3_path: str) -> dict:
    """
        Get a dictionary of fleet attributes: aircraft_type, wingspan
        Wingspan is determined based on OpenAP (if available), or otherwise using BADA3
        :param df:
        :param bada_3_path:
        :return: dict
    """
    agg_dict = {"typecode": "first"}
    if "APModel" in df.columns:
        agg_dict["APModel"] = "first"
    fleet_attributes = df.groupby("flight_id").agg(agg_dict).rename(columns={"typecode": "aircraft_type"}).reset_index()
    fleet_attributes["wingspan"] = fleet_attributes.apply(
        lambda d: get_wing_span(d["aircraft_type"], bada_3_path), axis=1
    )
    return fleet_attributes.set_index("flight_id").to_dict(orient="index")
