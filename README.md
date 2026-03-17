# jecats-paper-climate-mitigation


## Getting started
```
pip install -e .
```

### Aircraft performance
We use pycontrails-bada:
```
gcloud auth login
pip install keyring keyrings.google-artifactregistry-auth
pip install --index-url https://us-central1-python.pkg.dev/contrails-301217/pycontrails/simple \
    "pycontrails-bada==0.7.7"
```
More details [here](https://py.contrails.org/install.html#bada).

### aCCFs
We use [this](https://gitlab.tudelft.nl/jsmretschnig/accfs-fast) vectorized version of the aCCFs.
1. clone the repository
2. within the current `venv`, go to the cloned directory
3. once there, run `pip install -e .`


## Authors
- Jakob Smretschnig

## License
For open source projects, say how it is licensed.
