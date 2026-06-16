# CANE - Contrail Avoidance Non-CO2 Evaluation

<!--- Add here a badge for the ArXiv identifier of the pre-print version of the paper/journal-article
    related to this code project (arXiv:YYMM.NNNNN) (if applicable) e.g.:

    [![Paper](http://img.shields.io/badge/Paper-arXiv.YYMM.NNNNN-B3181B?logo=arXiv)](https://arxiv.org/abs/...)
-->

<!--- Add here the hyperlink to the finalized version of the paper/journal-article related to this project
    (the DOI link provided by the journal publisher after peer-review acceptance) (if applicable) e.g.:

    This repository is the official implementation of the following paper.

    * Paper title: [Paper Title](https://doi.org/YYMM.NNNNN)
-->

## Description

> This is a repository to evaluate the effect of contrail avoidance on the net climate benefit, considering CO2, contrails, NOx, and H2O.

> 4,112 flights traversing the Borealis region (Northern Europe) in 2023 are considered.

> Data accompanying the repository is available on [4TU.ResearchData]().

The repository accompanies the paper: _add reference to paper once published_

<!--- ## History

Provide a changelog (if applicable)
-->

## Authors or Maintainers

Jakob Smretschnig ([@jsmretschnig](https://github.com/jsmretschnig), ![ORCID logo](https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png) [0009-0003-6446-3039](https://orcid.org/0009-0003-6446-3039), j.smretschnig@tudelft.nl, Delft University of Technology, Delft, The Netherlands

<!--- ## Table of Contents Provide a table of contents to help readers navigate the README
-->

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

---

### 🔢 Data

#### ✈️ Trajectory data and simulation output

- Data accompanying the repository is available on 4TU.ResearchData.
- DOI: [10.4121/16ec2954-a493-41c8-b3f9-f17e9331c46b](https://10.4121/16ec2954-a493-41c8-b3f9-f17e9331c46b)

#### 🌐 Tropopause data

- Download the ERA5 tropopause data from Hoffmann and Spang (2021) for Fig. 6 [here](https://datapub.fz-juelich.de/slcs/tropopause/index.html).

#### 🌤️ Weather data

- Download the ERA5 hourly data on pressure levels / single levels from 1940 to present [here](https://cds.climate.copernicus.eu/datasets) or use the pycontrails interface [here](https://py.contrails.org/notebooks/ECMWF.html).

---

## Structure

Directory structure of `cane`:

```
.
└── notebooks
│   └── figure-*.ipynb
│   ├── logo.ipynb
└── src
    └── cane
        └── airspaces
        │   └── static
        │   │   └── Borealis_airspaces.json
        │   ├── borealis.py
        ├── colors.py
        ├── constants.py
        ├── labels.py
        ├── sankey.py
        ├── trajectory.py
        ├── utils.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
```

- `notebooks/figure-*.ipynb`: Each notebook represents one figure of the paper.
- `notebooks/logo.ipynb`: A notebook to plot the logo of the repository.
- `src/cane/airspaces/*`: To visualize the boundaries of the Borealis airspaces.
- `src/cane/*`: Helpers for coloring, constants, friendly names, haul-type classification etc.
- `src/cane/sankey.py`: This is a [pySankey](https://github.com/anazalea/pySankey/tree/master) fork with some bug-fixes.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The contents of this repository are licensed under a **MIT** license (see LICENSE file).

## Citation

If you want to cite this repository in your research paper, please use the following information:

Smretschnig, Jakob. "Contrail Avoidance Non-CO2 Evaluation (CANE) Code Repository." DOI: [10.4121/cbdafa47-709d-45da-86e1-7fed28ec3582](https://doi.org/10.4121/cbdafa47-709d-45da-86e1-7fed28ec3582). (2026).

## Would you like to contribute?

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

Special thanks to [Thymen](https://github.com/ThymenW) for the inspiration on the repository structure and to [Heather](https://github.com/HeatherAn) for recommended documentation practices.

## References

**algorithmic Climate Change Function (aCCF)**

Van Manen, J., and V. Grewe. “Algorithmic Climate Change Functions for the Use in Eco-Efficient Flight Planning.” Transportation Research Part D: Transport and Environment 67 (February 2019): 388–405. https://doi.org/10.1016/j.trd.2018.12.016.

Yin, Feijia, Volker Grewe, Federica Castino, et al. “Predicting the Climate Impact of Aviation for En-Route Emissions: The Algorithmic Climate Change Function Submodel ACCF 1.0 of EMAC 2.53.” Geoscientific Model Development 16, no. 11 (2023): 3313–34. https://doi.org/10.5194/gmd-16-3313-2023.

Dietmüller, Simone, Sigrun Matthes, Katrin Dahlmann, et al. “A Python Library for Computing Individual and Merged Non-CO 2 Algorithmic Climate Change Functions: CLIMaCCF V1.0.” Geoscientific Model Development 16, no. 15 (2023): 4405–25. https://doi.org/10.5194/gmd-16-4405-2023.

Matthes, Sigrun, Simone Dietmüller, Katrin Dahlmann, et al. “Updated Algorithmic Climate Change Functions (aCCF) V1.0A: Evaluation with the Climate-Response Model AirClim V2.0.” Preprint, Atmospheric sciences, 2023. https://doi.org/10.5194/gmd-2023-92.

**BADA3**

EUROCONTROL. User Manual for the Base of Aircraft Data (BADA) Revision 3.16. EIH Technical/Scientific Report No. 22/05/12-45. EUROCONTROL Experimental Centre (EEC), 2022.

**CoCiP**

U. Schumann. “A Contrail Cirrus Prediction Model.” Geoscientific Model Development 5, no. 3 (2012): 543–80. https://doi.org/10.5194/gmd-5-543-2012.

**Conversion factors**

Dahlmann, Katrin, Sigrun Matthes, and Volker Grewe. “Conversion of Climate Metrics for Policy Applications.” Preprint, Zenodo, July 31, 2025. https://doi.org/10.5281/ZENODO.16355781.

**DelftBlue**

DHCP: DelftBlue Supercomputer (Phase 2), https://www.tudelft.nl/dhpc/ark:/44463/DelftBluePhase2, delft High Performance Computing
Centre (DHPC), 2024.

**ERA5**

Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on pressure levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.bd0915c6](https://doi.org/10.24381/cds.bd0915c6) (Accessed on 15-06-2026)

Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on single levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.bd0915c6) (Accessed on 15-06-2026)

ECMWF HRES forecast data. © 2026 European Centre for Medium-Range Weather Forecasts (ECMWF): https://www.ecmwf.int/en/forecasts/datasets/set-i (Accessed on 15-06-2026)

**FFM2**

DuBois, Doug, and Gerald C. Paynter. “‘Fuel Flow Method2’ for Estimating Aircraft Emissions.” SAE Transactions 115 (2006): 1–14.

**pycontrails**

Shapiro, Marc, Zeb Engberg, Roger Teoh, Marc Stettler, Tom Dean, and Tristan Abbott. Pycontrails: Python Library for Modeling Aviation Climate Impacts. V. v0.54.11. Zenodo, released July 2025. https://doi.org/10.5281/zenodo.16575452.

**Tropopause data**

Hoffmann, L. and R. Spang, Reanalysis Tropopause Data Repository, DOI: [10.26165/JUELICH-DATA/UBNGI2](https://doi.org/10.26165/JUELICH-DATA/UBNGI2), Jülich DATA, V1, 2021.

**T4T2**

Teoh, Roger, Ulrich Schumann, Edward Gryspeerdt, et al. “Aviation Contrail Climate Effects in the North Atlantic from 2016–2021.” Atmospheric Chemistry and Physics 22, no. 16 (2022): 10919--10935. https://doi.org/10.5194/acp-22-10919-2022.

Teoh, Roger, Zebediah Engberg, Marc Shapiro, Lynnette Dray, and Marc E. J. Stettler. “The High-Resolution Global Aviation Emissions Inventory Based on ADS-B (GAIA) for 2019–2021.” Atmospheric Chemistry and Physics 24, no. 1 (2024): 725–44. https://doi.org/10.5194/acp-24-725-2024.
