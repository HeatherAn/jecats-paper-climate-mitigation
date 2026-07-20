# %% Hello!
print("Simulate aCCFs")

# %% Basic imports
import numpy as np
import pandas as pd
import xarray as xr
import os
import sys
import glob
import datetime
import argparse

# %% Fix paths
HOME = os.getenv("HOME")
REPOSITORY = f"{HOME}/gitlab/jecats-paper-climate-mitigation"
DATA = f"{HOME}/path_to_data"
SCRATCH = f"{HOME}/scratch"

sys.path.insert(0, f"{os.getenv('HOME')}/gitlab/jecats-paper-climate-mitigation/")
path = f"{os.getenv('HOME')}/gitlab/jecats-paper-climate-mitigation/scripts"

# %% Import packages
from pycontrails.core import Fleet
from pycontrails import MetDataset, MetDataArray

from cane.models import era5
from cane.utils import get_lat_lon_bounds
from cane.models.accf import ACCF as FastACCF

print("imports successful")

def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-day", type=int, required=True, help="Day 1 to 8")
    parser.add_argument("-version", type=str, required=True, help="filed or optimised")
    args = parser.parse_args()
    day = args.day
    version = args.version
    print("updated day and version:", day, version)
    return day, version

def main():
    day, version = parse_my_args()

    # %% Read traffic data
    df = pd.read_parquet(f"{DATA}/data/processed/{version}_trajectories_day{day}.parquet")
    fleet = Fleet(
        time=df.timestamp,
        data=df
    )
    print("fleet loaded: ", fleet.n_flights)

    # %% Get MET data
    pl, sl = era5.era5_all(
        era5.tbs_ex2[day - 1],
        era5.pressure_levels_150_to_1000_coarse,
        era5.ProductType.REANALYSIS.value
    )
    pl = MetDataset(era5.extend_dims(pl.data)) # extend longitude (180) and level (100, 1050)
    sl = MetDataset(era5.extend_longitude(sl.data)) # extend longitude (180)
    print("era5 loaded and extended")

    # %% Downscale MET data (and overwrite pl and sl!)
    lat_bounds, lon_bounds = get_lat_lon_bounds(df, df)

    pl = MetDataset(pl.data.sel(
        latitude=slice(lat_bounds[0], lat_bounds[1]),
        longitude=slice(lon_bounds[0], lon_bounds[1]),
        time=slice(fleet.time_start.floor("h"), fleet.time_end.ceil("h"))
    ))
    sl = MetDataset(sl.data.sel(
        latitude=slice(lat_bounds[0], lat_bounds[1]),
        longitude=slice(lon_bounds[0], lon_bounds[1]),
        time=slice(fleet.time_start.floor("h"), fleet.time_end.ceil("h"))
    ))
    print("era5 downscaled")

    # %% Compute fast aCCFs
    start_datetime = datetime.datetime.now()
    fastaccf = FastACCF(
        version="VANMANEN_GREWE_2019",
        efficacy="DAHLMANN_2025",
        era5_product_type="reanalysis",
        emission_scenario="pulse",
        time_horizon=20,
        include_pmo=False
    )
    o3_fast = fastaccf.accf_o3(
        geopotential=pl["geopotential"].data,
        temperature=pl["air_temperature"].data
    )
    ch4_fast = fastaccf.accf_ch4(
        geopotential=pl["geopotential"].data,
        timestamp=pl["time"].data.to_pandas(),
        latitude=pl["latitude"].data.values
    )
    nox_fast = o3_fast + ch4_fast
    h2o_fast = fastaccf.accf_h2o(
        potential_vorticity=pl["potential_vorticity"].data
    )
    co2_fast = fastaccf.accf_co2(fuel=1)  # only a constant float value
    end_datetime = datetime.datetime.now()
    print("fast accfs computed: ", end_datetime - start_datetime)

    # %% Intersect MET and aCCFs with waypoints
    for v in ["air_temperature", "specific_humidity", "eastward_wind", "northward_wind", "geopotential", "potential_vorticity", "relative_humidity"]:
        fleet[v] = fleet.intersect_met(pl[v])
    fleet["aCCF_O3"] = fleet.intersect_met(MetDataArray(o3_fast))
    fleet["aCCF_CH4"] = fleet.intersect_met(MetDataArray(ch4_fast))
    fleet["aCCF_NOx"] = fleet.intersect_met(MetDataArray(nox_fast))
    fleet["aCCF_H2O"] = fleet.intersect_met(MetDataArray(h2o_fast))
    fleet["aCCF_CO2"] = np.repeat(co2_fast, df.shape[0])
    print("MET and aCCFs intersected along waypoints")
    print(np.nansum(fleet["air_temperature"]))

    # %% Save the results
    saving_path = f"{SCRATCH}/{version}_trajectories_day{day}_with_accfs.parquet"
    fleet.dataframe.to_parquet(saving_path)
    print(f"dataframe saved to {saving_path}")


if __name__ == "__main__":
    main()
