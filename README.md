![Top Language](https://img.shields.io/github/languages/top/iporepos/apcac)
![Status](https://img.shields.io/badge/status-development-yellow.svg)
[![Code Style](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://iporepos.github.io/apcac/)
![Style Status](https://github.com/iporepos/apcac/actions/workflows/style.yaml/badge.svg)
![Docs Status](https://github.com/iporepos/apcac/actions/workflows/docs.yaml/badge.svg)
![Tests Status](https://github.com/iporepos/apcac/actions/workflows/tests.yaml/badge.svg)


---

# APCAC

This repository aims to organize the processing workflow for the classification of  
APCAC – *Priority Areas for Water Conservation* in the Cerrado biome in Brazil.

> [!NOTE]
> Check out the [documentation website](https://iporepos.github.io/apcac/) for more details.

# Installation

The Python modules maintained here are developed for the [QGIS 3](https://qgis.org/download/) environment.  
QGIS 3 should be installed in advanced mode, so that the following Python libraries are included:

- numpy  
- pandas  
- geopandas


# Running routines

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

> [!NOTE]
> Check out the [documentation website](https://iporepos.github.io/apcac/) for more details.

---

# Repo layout


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
│         └── data/               # run-time data
│
├── tests/                        # testing code folder
└── docs/                         # documentation folder

         

```
