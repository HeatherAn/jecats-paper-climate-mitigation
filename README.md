# REPOSITORY TITLE
CANE - Contrail Avoidance Non-CO2 Evaluation

## Description

This is a repository to evaluate the effect of contrail avoidance on the net climate benefit, considering CO2, contrails, NOx, and H2O. 4112 flights traversing the Borealis region (Northern Europe) in 2023 are considered.

The repository accompanies the results of the paper Smetschnig et al. (2026) (see **HOW TO CITE THIS DATASET**).

**Keywords:** Sustainable aviation - Contrail avoidance - Climate optimised trajectories - aCCF - CoCiP - pycontrails

**Date of data collection (YYYY-MM-DD):** 2025-01-01 until 2026-06-15

**Funding:** The project has been funded by CONCERTO under the SESAR 3 Joint Undertaking (Grant ID 101114785).

## AUTHORS

- **Jakob Smretschnig** ([@jsmretschnig](https://github.com/jsmretschnig), ![ORCID logo](https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png) [0009-0003-6446-3039](https://orcid.org/0009-0003-6446-3039), j.smretschnig@tudelft.nl, Delft University of Technology, Delft, The Netherlands

## ACCESS INFORMATION

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The contents of this repository are licensed under a **MIT** license (see LICENSE file).

### Repository DOI

Repository DOI: [10.4121/cbdafa47-709d-45da-86e1-7fed28ec3582](https://doi.org/10.4121/cbdafa47-709d-45da-86e1-7fed28ec3582)


## VERSIONING AND PROVENANCE

**Last modification date (YYYY-MM-DD):** 2026-07-20

## Requirements

### 📦 Installation

Clone the repository:

```bash
git clone git@gitlab.tudelft.nl:jsmretschnig/jecats-paper-climate-mitigation.git
cd jecats-paper-climate-mitigation
```

Create a virtual environment and activate it:

```bash
uv venv --python 3.11
source .venv/bin/activate
```

Install in editable mode:

```bash
uv pip install -e .
```

Check if `pip` and `uv` point to the same `.venv` directory:

```bash
source .venv/bin/activate # needs to be run again after pip install
which pip  # should point to .venv/bin/pip
```

Then install pycontrails-bada (because the last command doesn't work with `uv` prefix):

```bash
gcloud auth login
pip install keyring keyrings.google-artifactregistry-auth
pip install --index-url https://us-central1-python.pkg.dev/contrails-301217/pycontrails/simple \
    "pycontrails-bada==0.8.2"
```

More details [here](https://py.contrails.org/install.html#bada).

When using VS Code, make sure to select the venv's Python interpreter: Open the command palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) → Python: Select Interpreter → choose the one pointing to `.venv/bin/python`.


## FILE OVERVIEW

```
.
├── LICENSE
├── README.md
├── notebooks
│   ├── figure-*.ipynb
│   ├── methodology.ipynb
│   ├── pipeline.ipynb
│   ├── rq*.ipynb
│   └── table-*.ipynb
├── pyproject.toml
├── scripts
│   ├── run_accfs.py
│   └── run_cocip.py
└── src
    ├── cane
    │   ├── airspaces
    │   │   ├── borealis.py
    │   │   └── static
    │   │       └── Borealis_airspaces.json
    │   ├── colors.py
    │   ├── constants.py
    │   ├── labels.py
    │   ├── metrics
    │   │   ├── __init__.py
    │   │   ├── metrics.py
    │   │   └── static
    │   │       └── dahlmann-2025.csv
    │   ├── models
    │   │   ├── accf.py
    │   │   ├── aircraft_performance.py
    │   │   ├── cocip.py
    │   │   └── era5.py
    │   └── utils.py
```

- `notebooks/figure-*.ipynb`: Each notebook represents one figure of the paper.
- `notebooks/methodology.ipynb`: A notebook that represents results from the methodology section of the paper.
- `notebooks/pipeline.ipynb`: A notebook for the processing pipeline, from aircraft performance to climate models on a high-performance-computer (HPC), to climate metric calculations.
- `notebooks/rq*.ipynb`: Each notebook represents the numerical results for a research question.
- `notebooks/table*.ipynb`: Each notebook represents a table of the paper.
- `scripts/*`: Bash scripts to run aCCFs and CoCiP on a High-Performance-Computer (HPC), such as DelftBlue.
- `src/cane/airspaces/*`: To visualize the boundaries of the Borealis airspaces.
- `src/cane/metrics/*`: Compute the climate effect in different climate metrics.
- `src/cane/models/accf.py`: Compute the aCCFs for CO2, NOx, and H2O.
- `src/cane/models/aircraft_performance.py`: Compute the fuel consumption with BADA3.
- `src/cane/models/cocip.py`: Contains a helper for the CoCiP configuration.
- `src/cane/models/era5.py`: Download meteorological data from ERA5.
- `src/cane/*`: Helpers for coloring, constants, friendly names, haul-type classification etc.

Don't forget to fork [pySankey](https://github.com/anazalea/pySankey/tree/master) and remove the `check_data_matches_labels` part for the labels on the right side of the diagram in the code.

## HOW TO CITE THIS REPOSITORY

When using this repository please cite the **repository** and the **related article**:

_add reference to paper once published_  

Smretschnig, Jakob (2026): Repository to evaluate the effect of contrail avoidance on the net climate benefit (CO2, contrails, NOx, H2O) in Northern Europe. Version 1. 4TU.ResearchData. repository. https://doi.org/10.4121/cbdafa47-709d-45da-86e1-7fed28ec3582  


## REFERENCES

### DATASETS

[1] Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on pressure levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.bd0915c6](https://doi.org/10.24381/cds.bd0915c6)   

[2] Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on single levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.bd0915c6)   

[3] ECMWF HRES forecast data. © 2026 European Centre for Medium-Range Weather Forecasts (ECMWF): https://www.ecmwf.int/en/forecasts/datasets/set-i    

[4] Hoffmann, L. and R. Spang, Reanalysis Tropopause Data Repository, DOI: [10.26165/JUELICH-DATA/UBNGI2](https://doi.org/10.26165/JUELICH-DATA/UBNGI2), Jülich DATA, V1, 2021.


### OTHER

**algorithmic Climate Change Function (aCCF)**

[5] Van Manen, J., and V. Grewe. “Algorithmic Climate Change Functions for the Use in Eco-Efficient Flight Planning.” Transportation Research Part D: Transport and Environment 67 (February 2019): 388–405. https://doi.org/10.1016/j.trd.2018.12.016  

[6] Yin, Feijia, Volker Grewe, Federica Castino, et al. “Predicting the Climate Impact of Aviation for En-Route Emissions: The Algorithmic Climate Change Function Submodel ACCF 1.0 of EMAC 2.53.” Geoscientific Model Development 16, no. 11 (2023): 3313–34. https://doi.org/10.5194/gmd-16-3313-2023  

[7] Dietmüller, Simone, Sigrun Matthes, Katrin Dahlmann, et al. “A Python Library for Computing Individual and Merged Non-CO 2 Algorithmic Climate Change Functions: CLIMaCCF V1.0.” Geoscientific Model Development 16, no. 15 (2023): 4405–25. https://doi.org/10.5194/gmd-16-4405-2023  

[8] Matthes, Sigrun, Simone Dietmüller, Katrin Dahlmann, et al. “Updated Algorithmic Climate Change Functions (aCCF) V1.0A: Evaluation with the Climate-Response Model AirClim V2.0.” Preprint, Atmospheric sciences, 2023. https://doi.org/10.5194/gmd-2023-92  


**BADA3**

[9] EUROCONTROL. User Manual for the Base of Aircraft Data (BADA) Revision 3.16. EIH Technical/Scientific Report No. 22/05/12-45. EUROCONTROL Experimental Centre (EEC), 2022.  


**CoCiP**

[10] U. Schumann. “A Contrail Cirrus Prediction Model.” Geoscientific Model Development 5, no. 3 (2012): 543–80. https://doi.org/10.5194/gmd-5-543-2012.


**Conversion factors**

[11] Dahlmann, Katrin, Sigrun Matthes, and Volker Grewe. “Conversion of Climate Metrics for Policy Applications.” Preprint, Zenodo, July 31, 2025. https://doi.org/10.5281/ZENODO.16355781.


**FFM2**

[12] DuBois, D. and Paynter*, G., "“Fuel Flow Method2” for Estimating Aircraft Emissions," Non-Conference Specific Technical Papers - 2006, , https://doi.org/10.4271/2006-01-1987. 


**pyContrails**

[13] Shapiro, Marc, Zeb Engberg, Roger Teoh, Marc Stettler, Tom Dean, and Tristan Abbott. Pycontrails: Python Library for Modeling Aviation Climate Impacts. V. v0.54.11. Zenodo, released July 2025. https://doi.org/10.5281/zenodo.16575452.


**T4T2**

[14] Teoh, Roger, Ulrich Schumann, Edward Gryspeerdt, et al. “Aviation Contrail Climate Effects in the North Atlantic from 2016–2021.” Atmospheric Chemistry and Physics 22, no. 16 (2022): 10919--10935. https://doi.org/10.5194/acp-22-10919-2022.

[15] Teoh, Roger, Zebediah Engberg, Marc Shapiro, Lynnette Dray, and Marc E. J. Stettler. “The High-Resolution Global Aviation Emissions Inventory Based on ADS-B (GAIA) for 2019–2021.” Atmospheric Chemistry and Physics 24, no. 1 (2024): 725–44. https://doi.org/10.5194/acp-24-725-2024.
