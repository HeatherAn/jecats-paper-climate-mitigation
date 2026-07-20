"""algorithmic Climate Change Functions (aCCFs)"""

import numpy as np
import pandas as pd
import xarray as xr


class ACCF_Params:
    VALID_VERSIONS = [
        "VANMANEN_GREWE_2019", # van Manen and Grewe 2019
        "YIN_2023",  # Yin et al. 2023 / Dietmüller et al. 2023
        "MATTHES_2023"  # Matthes et al. 2023 (preprint) # TODO, test for Cont fails with e-31 numbers
    ]
    VALID_PRODUCT_TYPES = ["reanalysis", "ensemble"]
    VALID_EMISSION_SCENARIOS = ["pulse", "future"]
    VALID_TIME_HORIZONS = [20, 50, 100]
    VALID_EFFICACIES = ["LEE_2021", "DAHLMANN_2025"]

    scaling_factor = {
        "VANMANEN_GREWE_2019": {"CH4": 1, "O3": 1, "H2O": 1, "Cont": 1, "CO2": 1},
        "YIN_2023": {"CH4": 2.03, "O3": 1.97, "H2O": 1.92, "Cont": 1, "CO2": 1},
        "MATTHES_2023": {"CH4": 35, "O3": 11, "H2O": 3, "Cont": 3, "CO2": 1}
    }
    forecast_step = {
        "reanalysis": 1.0,
        "ensemble": 3.0
    }
    efficacy = {
        "LEE_2021": {"CH4": 1.18, "O3": 1.37, "H2O": 1, "Cont": 0.42},  # Lee 2021
        "DAHLMANN_2025": {"CH4": 1.04, "O3": 1.05, "H2O": 1, "Cont": 0.21}  # Ponater 2010, Ponater 2010, -, Bickel 2025
    }

    # Metric conversion: Dietmüller et al. 2023
    metric_conv = {
        "pulse": {
            20: {"CH4": 1, "O3": 1, "H2O": 1, "Cont": 1, "CO2": 1}
        },
        "future": {
            20: {"CH4": 10.8, "O3": 14.5, "H2O": 14.5, "Cont.": 13.6, "CO2": 9.4},
            50: {"CH4": 42.5, "O3": 34.1, "H2O": 34.1, "Cont.": 30.1, "CO2": 44.0},
            100: {"CH4": 98.2, "O3": 58.3, "H2O": 58.3, "Cont.": 48.9, "CO2": 125.0}
        }
    }


class ACCF:
    def __init__(
        self,
        version: str = "YIN_2023",
        era5_product_type: str = "reanalysis",
        emission_scenario: str = "pulse",
        time_horizon: int = 20,
        efficacy: str = "DAHLMANN_2025",
        include_pmo: bool = False
    ) -> None:
        """
        Initialize the ACCF class.
        """
        if version not in ACCF_Params.VALID_VERSIONS:
            raise ValueError(f"Invalid version: {version}. Must be one of {ACCF_Params.VALID_VERSIONS}.")
        if era5_product_type not in ACCF_Params.VALID_PRODUCT_TYPES:
            raise ValueError(f"Invalid product type: {era5_product_type}. Must be one of {ACCF_Params.VALID_PRODUCT_TYPES}.")
        if emission_scenario not in ACCF_Params.VALID_EMISSION_SCENARIOS:
            raise ValueError(f"Invalid emission scenario: {emission_scenario}. Must be one of {ACCF_Params.VALID_EMISSION_SCENARIOS}.")
        if time_horizon not in ACCF_Params.VALID_TIME_HORIZONS:
            raise ValueError(f"Invalid time horizon: {time_horizon}. Must be one of {ACCF_Params.VALID_TIME_HORIZONS}.")
        if efficacy not in ACCF_Params.VALID_EFFICACIES:
            raise ValueError(f"Invalid efficacy: {efficacy}. Must be one of {ACCF_Params.VALID_EFFICACIES}.")

        self.version = version
        self.era5_product_type = era5_product_type
        self.emission_scenario = emission_scenario
        self.time_horizon = time_horizon
        self.efficacy = efficacy
        self.include_pmo = include_pmo

    def accf_o3(
        self,
        geopotential: xr.DataArray,
        temperature: xr.DataArray
    ) -> xr.DataArray:
        """ Determines the O3 (ozone) aCCF.
            Args:
                geopotential (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: m2/s2)
                temperature (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: K)
            Returns:
                xarray.DataArray: 4D ("longitude", "latitude", "level", "time") O3 aCCF. (unit: K/kg(NO2))
        """
        # TODO according to paper, and without division through scaling_factor
        a = -2.64e-11
        b = 1.17e-13
        c = 2.46e-16
        d = -1.04e-18

        # CLIMaCCF
        a = -5.20e-11
        b = 2.30e-13
        c = 4.85e-16
        d = -2.04e-18

        accf = a + (b * temperature) + (c * geopotential) + (d * temperature * geopotential)
        accf = accf / ACCF_Params.scaling_factor[self.version]["O3"]
        accf = accf * ACCF_Params.efficacy[self.efficacy]["O3"]
        accf = xr.where(accf < 0, 0, accf)

        return accf.assign_attrs({
            "unit": "K kg(NO2)**-1",
            "long_name": "algorithmic climate change function of ozone",
            "short_name": "aCCF of ozone"
        })


    def accf_ch4(
        self,
        geopotential: xr.DataArray,
        timestamp: pd.DataFrame,
        latitude: np.ndarray
    ) -> xr.DataArray:
        """ Determines the CH4 (methane) aCCF.
            Args:
                geopotential (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: m2/s2)
                timestamp (pandas.DataFrame): Column "time" in pd.DateTime format.
                latitude (np.ndarray): Latitudes.
            Returns:
                xarray.DataArray: 4D ("longitude", "latitude", "level", "time") CH4 aCCF. (unit: K/kg(NO2))
        """
        # TODO according to paper, and without division through scaling_factor
        a = -4.84e-13
        b = 9.79e-19
        c = -3.11e-16
        d = 3.01e-21

        # CLIMaCCF
        a = -9.83e-13
        b = 1.99e-18
        c = -6.32e-16
        d = 6.12e-21

        def _f_in(n, phi):
            n_all = np.arange(365) + 1
            d_all = -23.44 * np.cos(np.deg2rad(360 / 365 * (n_all + 10)))

            cos_theta = np.outer(np.sin(np.deg2rad(phi)),
                                 np.sin(np.deg2rad(d_all[n - 1]))) + np.outer(np.cos(np.deg2rad(phi)),
                                                                              np.cos(np.deg2rad(d_all[n - 1])))
            f = 1360 * cos_theta
            return xr.DataArray(
                f,
                dims=["latitude", "time"],
                coords={"latitude": phi, "time": timestamp}
            )

        days = timestamp.dt.dayofyear.values - 1   # N begins with 0
        f_in = _f_in(days, latitude)

        accf = a + (b * geopotential) + (c * f_in) + (d * geopotential * f_in)
        accf = accf / ACCF_Params.scaling_factor[self.version]["CH4"]
        accf = accf * ACCF_Params.efficacy[self.efficacy]["CH4"]
        accf = xr.where(accf >= 0, 0, accf)

        return accf.assign_attrs({
            "unit": "K kg(NO2)**-1",
            "long_name": "algorithmic climate change function of methane",
            "short_name": "aCCF of methane"
        })


    def accf_nox(
        self,
        geopotential: xr.DataArray,
        temperature: xr.DataArray,
        timestamp: pd.DataFrame,
        latitude: np.ndarray
    ) -> xr.DataArray:
        """ Determines the NOx (ozone) aCCF.
            Args:
                geopotential (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: m2/s2)
                temperature (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: K)
                timestamp (pandas.DataFrame): Column "time" in pd.DateTime format.
                latitude (array): Latitudes.
            Returns:
                xarray.DataArray: 4D ("longitude", "latitude", "level", "time") NOx aCCF. (unit: K/kg(NO2))
        """
        o3 = self.accf_o3(geopotential, temperature)
        ch4 = self.accf_ch4(geopotential, timestamp, latitude)
        nox = o3 + ch4
        return nox.assign_attrs({
            "unit": "K kg(NO2)**-1",
            "long_name": "algorithmic climate change function of NOx emission",
            "short_name": "aCCF of  NOx emission"
        })

    def accf_pmo(
        self,
        ch4
    ):
        return 0.29 * ch4

    def accf_h2o(
        self,
        potential_vorticity: xr.DataArray
    ):
        """ Determines the H2O aCCF.
            Args:
                potential_vorticity (xarray.DataArray): Dimensions must be: "longitude", "latitude", "level", "time". (unit: K m2 kg-1 s-1)
            Returns:
                xarray.DataArray: 4D ("longitude", "latitude", "level", "time") H2O aCCF. (unit: K/kg(fuel))
        """
        # TODO according to paper, and without division through scaling_factor
        # accf = 2.11e-16 + 7.7e-17 * np.absolute(potential_vorticity)

        # CLIMaCCF
        accf = 4.05e-16 + 1.48e-16 * np.absolute(potential_vorticity * 1e6)  # pv * 1e6 = [PVU]
        accf = accf / ACCF_Params.scaling_factor[self.version]["H2O"]
        accf = accf * ACCF_Params.efficacy[self.efficacy]["H2O"]
        return accf.assign_attrs({ # TODO naming
            "unit": "K kg(fuel)**-1",
            "long_name": "algorithmic climate change function of water vapor",
            "short_name": "aCCF of water vapor"
        })
