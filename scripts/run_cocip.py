# %% Hello!
print("Simulate CoCiP")

# %% Basic imports
import numpy as np
import pandas as pd
import xarray as xr
import os
import glob
import argparse
import datetime

# %% Fix paths
HOME = os.getenv("HOME")
REPOSITORY = f"{HOME}/gitlab/jecats-paper-climate-mitigation"
SCRATCH = f"{HOME}/scratch"
DATA = f"{SCRATCH}/traffic/data/processed"
BADA_3_PATH = f"{HOME}/BADA3.16"

# %% Import packages
from pycontrails import Flight, MetDataset
from pycontrails.models.cocip import Cocip

from mpi4py import MPI

from cane.models import era5
from cane.models.cocip import humidity_scaling
from cane.utils import df_to_flight

print("imports successful")


def compute_cocip(flight: Flight, pl: MetDataset, sl: MetDataset, **kwargs) -> Flight:
    rank = MPI.COMM_WORLD.Get_rank()

    # kwargs
    day = kwargs["day"]
    version = kwargs["version"]

    start_datetime = datetime.datetime.now()
    fid = flight.dataframe.flight_id.values[0]

    # skip if already computed
    if f"{version}_trajectories_day{day}_with_accfs_and_cocip_{fid}.parquet" in os.listdir(f"{DATA}/day{day}"):
        print(f"Rank {rank} found flight number: {fid} - skipping")
        return Flight(
            pd.read_parquet(f"{DATA}/day{day}/{version}_trajectories_day{day}_with_accfs_and_cocip_{fid}.parquet")
            .rename(columns={
                "eastward_wind": "u_wind",
                "northward_wind": "v_wind",
            })
        )

    print(f"Rank {rank} processing flight number: {fid}")
    cocip = Cocip(
        met=pl, rad=sl,
        params={
            "dt_integration": np.timedelta64(10, "m"),
            "max_age": np.timedelta64(12, "h"),
            "humidity_scaling": humidity_scaling,
            "compute_atr20": True
        }
    )
    cocip_out = cocip.eval(flight)

    # save results
    # make sure all meta data are serializable (np.int is not allowed, but int is; for whatever reason np.float works fine)
    cocip_out.attrs = {
        k: int(v) if isinstance(v, np.integer) else v
        for k, v in cocip_out.attrs.items()
    }
    cocip_out.dataframe.to_parquet(
        f"{DATA}/day{day}/{version}_trajectories_day{day}_with_accfs_and_cocip_{fid}.parquet")  # includes the .attrs :))

    end_datetime = datetime.datetime.now()
    print(f"Rank {rank}: cocip computed for flight_id: ", fid, "in: ", end_datetime - start_datetime)
    return cocip_out


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

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(size, rank)

    if rank == 0:
        # %% Read traffic data
        df = (
            pd.read_parquet(f"{DATA}/{version}_trajectories_day{day}_with_accfs.parquet")
            .rename(columns={
                "eastward_wind": "u_wind",
                "northward_wind": "v_wind",
            })
        )
        print("fleet loaded, day: ", day, "version: ", version)

        # Create output dirs
        path_to_output = os.path.expanduser(f"{DATA}/day{day}")
        os.makedirs(path_to_output, exist_ok=True)

        # Convert to fleet
        fleet = {
            fid: df_to_flight(group, bada_3_path=BADA_3_PATH) # BADA3 is required for adding the wingspan
            for fid, group in df.groupby("flight_id")
        }
        flights = list(fleet.values())

        # Split flights among ranks
        chunk_size = len(flights) // size
        chunks = []
        for r in range(size):
            start = r * chunk_size
            end = (r + 1) * chunk_size if r != size - 1 else len(flights)
            chunks.append(flights[start:end])
            print(f"Rank {r} gets slice {start}:{end}")
    else:
        chunks = None

    # Scatter the chunks across ranks
    my_flights = comm.scatter(chunks, root=0)
    print(f"Rank {rank} received {len(my_flights)} flights")

    # %% Get MET data
    pl, sl = era5.era5_all(
        era5.tbs_ex2[day - 1],
        era5.pressure_levels_150_to_1000_coarse,
        era5.ProductType.REANALYSIS.value
    )
    print("era5 loaded")

    # %% Compute CoCiP
    print("Start to compute cocip")
    cocip_flights = [
        compute_cocip(flight=flight, pl=pl, sl=sl, day=day, version=version)
        for flight in my_flights
    ]
    print("cocip computed!")

    # All results
    all_cocip_flights = comm.gather(cocip_flights, root=0)
    if rank == 0:
        print("flights gathered")


if __name__ == "__main__":
    main()
