import numpy as np
import pandas as pd
from pycontrails.core import Flight as PyFlight
from pycontrails.ext.bada import BADAFlight

bada_3_path = ""  # TODO insert path


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
