![Top Language](https://img.shields.io/github/languages/top/iporepos/apcac)
![Status](https://img.shields.io/badge/status-development-yellow.svg)
[![Code Style](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://iporepos.github.io/apcac/)
![Style Status](https://github.com/iporepos/apcac/actions/workflows/style.yaml/badge.svg)
![Docs Status](https://github.com/iporepos/apcac/actions/workflows/docs.yaml/badge.svg)
![Tests Status](https://github.com/iporepos/apcac/actions/workflows/tests.yaml/badge.svg)


---

# APCAC

This repository organizes the processing workflow for the classification of
APCAC – *Priority Areas for Water Conservation* in the Cerrado biome in Brazil.
It is intended for researchers and environmental analysts working with geospatial
data in the QGIS environment.

> [!NOTE]
> Check out the [documentation website](https://iporepos.github.io/apcac/) for more details.

## Installation

The Python modules maintained here are developed for the [QGIS 3](https://qgis.org/download/) environment.
Install QGIS 3 in **advanced mode** so that the following Python libraries are included:

- numpy
- pandas
- geopandas

> [!TIP]
> See the [QGIS installation guide](https://qgis.org/resources/installation-guide/) for instructions on
> installing QGIS with the advanced (OSGeo4W) installer, which bundles the required Python libraries.

Once QGIS is installed, clone this repository:

```bash
git clone https://github.com/iporepos/apcac.git
```

## Running routines

The routines are developed as Python functions.
These functions must be executed through the QGIS Python Script tool,
using scripts with the following structure:

```python
# use the importlib library
import importlib.util as iu

# specify the module
the_module = "path/to/the/module.py"
spec = iu.spec_from_file_location("module", the_module)
module = iu.module_from_spec(spec)
spec.loader.exec_module(module)

# Now call the function
module.process_data(
    input1="path/to/data1.tif",
    input2="path/to/data2.tif",
    output_folder="path/to/results"
)
```

## Repo layout


```txt
apcac/
│
├── LICENSE
├── README.md                     # this file (landing page)
├── .gitignore                    # configuration of git
├── pyproject.toml                # configuration of python project
├── MANIFEST.in                   # configuration of source distribution
│
├── src/                          # source code folder
│    └── apcac/                   # source code root
│         ├── indexes.py          # module for handling indexes maps
│         ├── classes.py          # module for handling APCAC classification
│         └── data/               # run-time reference data (e.g. biome boundaries, lookup tables)
│
├── tests/                        # testing code folder
└── docs/                         # documentation folder
```

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).