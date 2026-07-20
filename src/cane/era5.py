import xarray as xr

from pycontrails.datalib.ecmwf import ERA5
from pycontrails.core.met import MetDataset
from pycontrails.models.cocip import Cocip
from pycontrails.models.accf import ACCF
from pycontrails.datalib import ecmwf

from enum import Enum


class ProductType(Enum):
    REANALYSIS = "reanalysis"
    ENSEMBLE_MEMBERS = "ensemble_members"


# pycontrails_37
supported_pressure_levels = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750,
                             700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225,
                             200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7,
                             5, 3, 2, 1, -1]

# pycontrails_27
pressure_levels_100_to_1000 = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450,
                               400, 350, 300, 250, 225, 200, 175, 150, 125, 100]

# pycontrails_20
pressure_levels_150_to_1000_coarse = [
    1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250,
    225, 200, 175, 150
]

# aCCFs
supported_pressure_levels_accf = [150, 175, 200, 225, 250, 300, 350, 400]

# CONCERTO ex2 days
tbs_ex2 = [
    ('2023-03-17 00:00:00', '2023-03-21 00:00:00'),
    ('2023-06-06 00:00:00', '2023-06-10 00:00:00'),
    ('2023-06-12 00:00:00', '2023-06-16 00:00:00'),
    ('2023-09-01 00:00:00', '2023-09-05 00:00:00'),
    ('2023-09-15 00:00:00', '2023-09-19 00:00:00'),
    ('2023-12-15 00:00:00', '2023-12-19 00:00:00'),
    ('2023-12-20 00:00:00', '2023-12-24 00:00:00'),
    ('2023-12-26 00:00:00', '2023-12-30 00:00:00')
]
friendly_days = [
    '2023-03-18 & 19',
    '2023-06-07 & 08',
    '2023-06-13 & 14',
    '2023-09-02 & 03',
    '2023-09-16 & 17',
    '2023-12-16 & 17',
    '2023-12-21 & 22',
    '2023-12-27 & 28'
]


def era5_all(time_bounds: tuple, pressure_levels: list, product_type: str = "reanalysis") -> tuple[
    MetDataset, MetDataset]:
    # pressure level data
    era5_pl = ERA5(
        time=time_bounds,
        variables=Cocip.met_variables + Cocip.optional_met_variables + (ACCF.met_variables[2], ACCF.met_variables[4]),
        pressure_levels=pressure_levels,
        product_type=product_type
    )

    # single level data (radiation)
    era5_sl = ERA5(
        time=time_bounds,
        variables=Cocip.rad_variables + (ecmwf.SurfaceSolarDownwardRadiation,),
        product_type=product_type
    )

    pl = era5_pl.open_metdataset()
    sl = era5_sl.open_metdataset()
    return pl, sl



def extend_longitude(ds: xr.Dataset) -> xr.Dataset:
    """
        Add longitude of 180 for interpolation.
    :param ds:
    :return:
    """
    ds_new = xr.concat([ds, ds.isel(longitude=-1).expand_dims(longitude=[180])], dim="longitude")  # pos N
    return ds_new.transpose(*list(ds.dims))


def extend_level(ds: xr.Dataset) -> xr.Dataset:
    """
        Add levels of 100 hPa and 1050 hPa for interpolation.
    :param ds:
    :return:
    """
    ds_new = xr.concat([ds, ds.isel(level=-1).expand_dims(level=[1050])], dim="level")  # pos N
    ds_new = xr.concat([ds_new.isel(level=0).expand_dims(level=[100]), ds_new], dim="level")  # pos 0
    return ds_new.transpose(*list(ds.dims))


def extend_dims(ds: xr.Dataset) -> xr.Dataset:
    """
        Add longitude and levels as in extend_longitude() and extend_level().
    :param ds:
    :return:
    """
    return ds.pipe(extend_longitude).pipe(extend_level)
