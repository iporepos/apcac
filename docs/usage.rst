.. _usage:

.. include:: ./includes/warning_dev.rst

User Guide
#######################################################################

.. seealso::

   For those who want to contribute, see :ref:`Development <development>`


This guide explains how to use the scripts in this repository to perform **APCAC** classification on polygons using vector and raster data. The scripts are designed to run within **QGIS** via the Python Script Tool, supporting both full workflow execution and independent function calls for custom analyses.

.. note::

    This repository is intended to run under the QGIS Python environment.

Installation
------------

1. Install **QGIS** in advanced mode.
2. During installation, ensure that the following **Python libraries** are installed in the QGIS environment:
   - ``numpy``
   - ``pandas``
   - ``geopandas``

These are the only external dependencies required to run the scripts.

Workflow
-----------------

The repository is structured as a **function-based workflow**, allowing:

* Full APCAC analysis from raster sampling to classification and reporting.
* Independent function calls for hydrology and erosion indices, fuzzification, and risk classification.
* Automatic management of timestamped output folders for reproducible runs and organized outputs.
* Easy integration into QGIS Python tools using ``importlib``.

Scripts operate on raster and vector data, with each catchment receiving
a full set of computed attributes. Outputs can be upscaled to
coarser maps or used for further GIS analysis.

Output Attributes
-------------------

The ultimate output of this process is the map of APCAC sampled at polygons, like small catchments or any other scale
of interest. The polygon layer is stored in a **geopackage** with the following core attributes:

.. csv-table::
   :file: ./data/fields.csv
   :header-rows: 1
   :widths: auto
   :delim: ;


Scripts
-------------------

Scripts are executed via the **Python Script Tool** in QGIS using the **importlib** workflow.

.. seealso::

    More scripts examples are available at the :ref:`API <development>`


The following example shows how to use the ``analysis_apcac()`` tool:

.. code-block:: python

    # WARNING : run this under a QGIS Python Environment
    import importlib.util as iu

    # define the paths to this module
    the_module = "path/to/classes.py"

    # setup module with importlib
    spec = iu.spec_from_file_location("module", the_module)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    # define the paths to input and output folders
    input_dir = "path/to/input_folder"
    output_dir = "path/to/output_folder"

    # define the path to input database
    input_db = "path/to/data.gpkg"

    # define the paths to input rasters
    raster_files = {
        "t": "path/to/raster_t.tif",
        "s": "path/to/raster_s.tif",
        "g": "path/to/raster_g.tif",
        "c": "path/to/raster_c.tif",
        "n": "path/to/raster_n.tif",
        "v": "path/to/raster_v.tif",
        "slope": "path/to/raster_slope.tif",
        "uslek": "path/to/raster_uslex.tif",
    }

    raster_multipliers = {
        "t": 1000,
        "s": 100,
        "slope": 100,
    }

    # call the full APCAC analysis
    module.analysis_apcac(
        input_db=input_db,
        input_layer="apcac_bho5k",
        raster_files=raster_files,
        output_folder=output_dir,
        raster_multipliers=raster_multipliers,
        cleanup=True
    )

Notes
---------

* Users can call individual functions for **custom analyses** instead of running the full workflow.
* All outputs are organized in **timestamped folders** for reproducibility.
* Raster maps form the base for calculations, and **zonal statistics** are applied to catchments for final aggregation.
* No additional external dependencies are required beyond ``numpy``, ``pandas``, and ``geopandas``.

