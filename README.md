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
APCAC – *Priority Areas for Water Conservation in the Cerrado*.

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
These functions must be executed through the QGIS “Run Script” tool,  
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
copyme/
│
├── LICENSE
├── README.md                     # [CHECK THIS] this file (landing page)
├── .gitignore                    # [CHECK THIS] configuration of git vcs ignoring system
├── pyproject.toml                # [CHECK THIS] configuration of python project
├── MANIFEST.in                   # [CHECK THIS] configuration of source distribution
│
├── .venv/                        # [ignored] virtual environment (recommended for development)
│
├── .github/                      # github folder
│    └── workflows/               # folder for continuous integration services
│         ├── style.py            # [CHECK THIS] configuration file for style check workflow
│         ├── tests.py            # [CHECK THIS] configuration file for tests workflow
│         └── docs.yml            # [CHECK THIS] configuration file for docs build workflow
│
├── src/                          # source code folder
│    ├── apcac.egg-info          # [ignored] [generated] files for local development
│    └── apcac/                  # [CHANGE THIS] source code root
│         ├── __init__.py         # template init file
│         ├── variables.py        
│         ├── indexes.py        
│         ├── classes.py        
│         └── data/               # run-time data
│              └── src_data.txt   # dummy data file
│
├── tests/                        # testing code folder
│    ├── conftest.py              # [CHECK THIS] configuration file of tests
│    ├──unit/                     # unit tests package     
│    │    ├── __init__.py
│    │    └── test_module.py      # template module for unit tests
│    ├── bcmk/                    # benchmarking tests package
│    │    ├── __init__.py               
│    │    └── test_bcmk.py        # template module for benchmarking tests
│    ├── data/                    # test-only data
│    │     ├── test_data.csv
│    │     ├── datasets.csv       # table of remote datasets
│    │     └── dataset1/          # [ignored] subfolders in data
│    └── outputs/                 # [ignored] tests outputs
│
└── docs/                         # documentation folder
     ├── docs_update.rst          # updating script
     ├── about.rst                # info about the repo
     ├── conf.py                  # [CHECK THIS] configuration file for sphinx
     ├── dummy.md                 # markdown docs also works
     ├── index.rst                # home page for documentation
     ├── usage.rst                # instructions for using this repo
     ├── figs/                    # figs-only files
     │    ├── logo.png
     │    ├── logo.svg
     │    └── fig1.png               
     ├── data/                    # docs-only data
     │    └── docs.txt            # dummy data file
     ├── generated/               # [generated] sphinx created files 
     ├── _templates/              # [ignored] [generated] sphinx created stuff
     ├── _static/                 # [ignored] [generated] sphinx created stuff
     └── _build/                  # [ignored] [generated] sphinx build
         

```
