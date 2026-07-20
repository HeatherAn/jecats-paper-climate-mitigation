import numpy as np
import pandas as pd
import pathlib
from enum import Enum

from pycontrails import Fleet

from cane import constants
from cane.models.accf import day_contrail_RF, night_contrail_RF, contrail_RF
from cane.utils import mask_by_validity_range, mask_by_marker

# K. Dahlmann et al. 2025 (preprint)
_path_to_static = pathlib.Path(__file__).parent / "static"
CONVERSION_FACTORS_PULSE = CF = (
    pd.read_csv(_path_to_static / "dahlmann-2025.csv", index_col=0).transpose().to_dict()
)

class AGWP_CO2_100y(Enum):
    # [W m^-2 year kg_CO2^-1]
    JOOS_2013 = 92.5e-15  # [58, 117]
    GAILLOT_2023 = 88.0e-15


ATR100_dahlmann = 5.148e-16 # Dahlmann et al. 2025


class AGWP_CO2_20y(Enum):
    # [W m^-2 year kg_CO2^-1]
    GAILLOT_2023 = 2.39e-14


# divide the aCCF value by this factor
backward_calculation_factors = {
    "H2O": 0.520, "O3": 0.508, "CH4": 0.492, "CiC": 0.509
}


class Metrics:
    def __init__(self, origin: str, target: str, emission_scenario: str = "pulse"):
        if origin not in list(CF.keys()) + ["RF"] or target not in CF.keys():
            raise ValueError("origin and target must be in CF dictionary")
        if emission_scenario != "pulse":
            raise ValueError("emission_scenario must be pulse, no others supported until now")

        self.origin = origin
        self.target = target
        self.emission_scenario = emission_scenario

        if self.origin == "RF":
            self.cf = {
                "CO2": CF[target]["CO2"],
                "H2O": CF[target]["H2O"],
                "O3": CF[target]["O3"],
                "CH4": CF[target]["CH4"],
                "PMO": CF[target]["PMO"],
                "CiC": CF[target]["CiC"],
            }
        else:
            self.cf = {
                "CO2": CF[target]["CO2"] / CF[origin]["CO2"],
                "H2O": CF[target]["H2O"] / CF[origin]["H2O"],
                "O3": CF[target]["O3"] / CF[origin]["O3"],
                "CH4": CF[target]["CH4"] / CF[origin]["CH4"],
                "PMO": CF[target]["PMO"] / CF[origin]["PMO"],
                "CiC": CF[target]["CiC"] / CF[origin]["CiC"],
            }


def eagwp_from_contrail_ef(ef: float | np.ndarray[float], erf_rf_ratio: float = 1.0) -> float:
    """
        :param ef: EF in [J]
        :param erf_rf_ratio: 0.42 to convert RF to ERF (efficacy, Lee et al. 2021), otherwise 1.0
        :return: AGWP in [W m^-2 year]
    """
    return (ef / constants.surface_area_earth / constants.seconds_per_year) * erf_rf_ratio

def compute_metrics_for_fleet(
    fleet: Fleet,
    accf_scaling: dict,
    accf_bounds: tuple,
    efficacy: dict,
    target: str
) -> Fleet:
    m = Metrics(origin="RF", target=target, emission_scenario="pulse")
    m2 = Metrics(origin="ATR20", target=target, emission_scenario="pulse")

    # (also calculate) Contrail aCCF
    fleet["rf_day"] = day_contrail_RF(fleet["olr_mean"] * -1, fleet["sdr_mean"])
    fleet["rf_night"] = night_contrail_RF(fleet["air_temperature"], fleet["sdr_mean"])
    fleet["rf_CiC"] = contrail_RF(fleet["rf_night"], fleet["rf_day"], fleet["sac"]) * efficacy["CiC"] / scaling["CiC"]
    fleet.update({"rf_CiC": fleet["rf_CiC"] * fleet.segment_length() / 1e3})
    mask_by_validity_range(fleet, ["rf_CiC"], bounds=accf_bounds)  # W m^-2 km^-1
    fleet["CiC"] = fleet["rf_CiC"] * m.cf["CiC"]

    # CoCiP
    fleet["eagwp_cocip"] = eagwp_from_contrail_ef(fleet["ef"], efficacy["CiC"])
    fleet["rf_cocip"] = fleet["eagwp_cocip"] / 0.21  # to get from EAGWP to RF
    fleet["CoCiP"] = fleet["rf_cocip"] * m.cf["CiC"]

    # aCCF
    # apply mask
    mask_by_validity_range(fleet, ["aCCF_O3", "aCCF_CH4", "aCCF_H2O"], bounds=accf_bounds)

    fleet["O3"] = fleet["aCCF_O3"] * fleet["nox_ei"] * fleet["fuel_burn"] * efficacy["O3"] / scaling["O3"] * m2.cf["O3"]
    fleet["CH4"] = fleet["aCCF_CH4"] * fleet["nox_ei"] * fleet["fuel_burn"] * efficacy["CH4"] / scaling["CH4"] * m2.cf["CH4"]
    fleet["H2O"] = fleet["aCCF_H2O"] * fleet["fuel_burn"] * efficacy["H2O"] / scaling["H2O"] * m2.cf["H2O"]
    fleet["NOx"] = fleet["O3"] + fleet["CH4"]
    cols = [
        'CO2', 'CO2_with_aCCF', 'CoCiP', 'CiC',
        'NOx', 'O3', 'CH4', 'H2O',
    ]
    cols_non_co2 = [
        'CO2_with_aCCF',
        'CoCiP', 'CiC',
        'NOx', 'O3', 'CH4', 'H2O',
    ]

    # CO2
    fleet["CO2"] = fleet["co2"]  # always CO2e
    fleet["CO2_with_aCCF"] = fleet["aCCF_CO2"] * fleet["fuel_burn"] * m2.cf["CO2"]

    if ver in ["yin_2023", "matthes_2023"]:
        fleet.update({"CiC": fleet["CiC"] / backward_calculation_factors["CiC"]})
        fleet.update({"O3": fleet["O3"] / backward_calculation_factors["O3"]})
        fleet.update({"CH4": fleet["CH4"] / backward_calculation_factors["CH4"]})
        fleet.update({"NOx": fleet["O3"] + fleet["CH4"]})
        fleet.update({"H2O": fleet["H2O"] / backward_calculation_factors["H2O"]})

    for col in cols_non_co2:
        co2eq = None
        if target == "EAGWP100" or target == "AGWP100":
            co2eq = fleet[col] / AGWP_CO2_100y.GAILLOT_2023.value
        elif target == "EAGWP20" or target == "AGWP20":
            co2eq = fleet[col] / AGWP_CO2_20y.GAILLOT_2023.value
        elif target == "ATR100":
            co2eq = fleet[col] / ATR100_dahlmann
        else:
            raise ValueError(f"Unknown target {target}")
        fleet.update({col: co2eq})

    if accf_bounds != [0, 1000]:
        mask_by_marker(fleet, ["NOx", "O3", "CH4", "H2O", "CiC"])  # not sure about CiC, but better be save

    return fleet
