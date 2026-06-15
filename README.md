# CANE - Contrail Avoidance Non-CO2 Evaluation

> This is a repository to evaluate the effect of contrail avoidance on the net climate benefit, considering CO2, contrails, NOx, and H2O.

> 4,112 flights traversing the Borealis region (Northern Europe) in 2023 are considered.

> Data accompanying the repository is available on [4TU.ResearchData]().

## 👨‍💻 Current status

Runtime on DelftBlue:

- Day 1, 221 flights, 58 minutes --> 1:15
- Day 2, 380 flights, 99 minutes --> 2h
- Day 3, 154 flights, 40 minutes --> 1:15
- Day 4, 340 flights, 89 minutes --> 2h
- Day 5, 1092 flights, 285 minutes --> 5h (and also with 12 cores)
- Day 6, 931 flights, 243 minutes --> 4:15 --> CPU 22%, memory 96%
- Day 7, 952 flights, 248 minutes --> 4:15
- Day 8, 520 flights, 136 minutes --> 2:30

### Action items

- [x] Get all notebooks producing figures working in this repo
- [ ] Move the notebooks for tables and RQs as well
- [x] Make the path to the data clear

---

## 📦 Installation

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

## 🔢 Data

### ✈️ Trajectory data and simulation output

- Data accompanying the repository is available on 4TU.ResearchData.
- DOI: [10.4121/16ec2954-a493-41c8-b3f9-f17e9331c46b](https://10.4121/16ec2954-a493-41c8-b3f9-f17e9331c46b)

### 🌐 Tropopause data

- Hoffmann, L. and R. Spang, Reanalysis Tropopause Data Repository, DOI: [10.26165/JUELICH-DATA/UBNGI2](https://doi.org/10.26165/JUELICH-DATA/UBNGI2), Jülich DATA, V1, 2021.
- Download the ERA5 tropopause data for Fig. 6 [here](https://datapub.fz-juelich.de/slcs/tropopause/index.html).

### 🌤️ Weather data

- Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on pressure levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.bd0915c6](https://doi.org/10.24381/cds.bd0915c6) (Accessed on 15-06-2026)

- Copernicus Climate Change Service, Climate Data Store, (2023): **ERA5 hourly data on single levels from 1940 to present**. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.bd0915c6) (Accessed on 15-06-2026)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under ... <!-- the terms of the Appache 2.0 [LICENSE](./LICENSE). -->

---

## 🙏 Acknowledgements

Special thanks to [Thymen](https://github.com/ThymenW) for the inspiration on the repository structure.
