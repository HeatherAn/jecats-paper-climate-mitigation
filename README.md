# CANE - Contrail Avoidance Non-CO2 Evaluation

> This is a repository to evaluate the effect of contrail avoidance on the total mitigation gain (CO2, Contrails, NOx, H2O).

> 4,112 flights traversing the Borealis region in 2023 are considered.

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

- [ ] Get all notebooks producing figures working in this repo
- [ ] Rename the flight IDs and remove callsigns and engine IDs

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

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under ... <!-- the terms of the Appache 2.0 [LICENSE](./LICENSE). -->

---

## 🙏 Acknowledgements

Special thanks to [Thymen](https://github.com/ThymenW) for the inspiration on the repository structure.
