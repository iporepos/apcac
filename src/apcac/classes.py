# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2025 The Project Authors
# See pyproject.toml for authors/maintainers.
# See LICENSE for license details.
"""
Complete workflow to perform ``APCAC`` classification on polygons using vector and raster data.

It is designed for use within ``QGIS`` via the Python script tool, allowing both full
workflow execution and independent function calls for custom analyses.

.. warning::

    This module is intended to run under the QGIS Python Environment.


.. important::

    The following external Python dependencies must be installed in the
    QGIS Environment via advanced mode: ``numpy``, ``pandas`` and ``geopandas``


Features
--------
* Orchestrate a full ``APCAC`` analysis, from raster sampling to classification and LaTeX report.
* Modular functions to compute hydrology and erosion indexes, fuzzification, and risk classification.
* Automatic management of timestamped output folders for reproducible runs and organized outputs.
* Easy integration into QGIS Python tools using ``importlib``, with no external installation required.

Overview
--------
The module defines the main processing steps as functions. Each function creates an output folder
with a timestamp for easy tracking. Users may run the full workflow through ``analysis_apcac``
or call individual functions independently for more
customized analyses.

Script Example
--------------

The following script runs a full ``APCAC`` analysis:

.. code-block:: python

    import importlib.util as iu

    # define the paths to this module
    # ----------------------------------------
    the_module = "path/to/classes.py"

    # setup module with importlib
    # ----------------------------------------
    spec = iu.spec_from_file_location("module", the_module)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    # define the paths to input and output folders
    # ----------------------------------------
    input_dir = "path/to/input_folder"
    output_dir = "path/to/output_folder"

    # define the path to input database
    # ----------------------------------------
    input_db = "path/to/data.gpkg"

    # define the paths to input rasters
    # ----------------------------------------
    raster_files = {
        # change this paths
        "t": "path/to/raster_t.tif", # topography layer
        "s": "path/to/raster_s.tif", # soil/pedology layer
        "g": "path/to/raster_g.tif", # geology/aquifers layer
        "c": "path/to/raster_c.tif", # climate layer
        "n": "path/to/raster_n.tif", # conservation layer
        "v": "path/to/raster_v.tif", # anthropic risk layer
        "slope": "path/to/raster_slope.tif", # terrain slope layer
        "uslek": "path/to/raster_uslex.tif", # erodibility layer
    }

    # define which index has multipliers (the value is divided)
    # ----------------------------------------
    raster_multipliers = {
        "t": 1000,
        "s": 100,
        "slope": 100,
        # change and add more if needed
    }

    # call the function
    # ----------------------------------------
    module.analysis_apcac(
        input_db=input_db,
        input_layer="apcac_bho5k",
        raster_files=raster_files,
        output_folder=output_dir,
        raster_multipliers=raster_multipliers ,
        cleanup=True
    )


"""
# IMPORTS
# ***********************************************************************
# import modules from other libs

# Native imports
# =======================================================================
import os, shutil
import time, datetime
import textwrap
from pathlib import Path

# ... {develop}

# External imports
# =======================================================================
import numpy as np
import pandas as pd
import geopandas as gpd
import processing

# ... {develop}

# Project-level imports
# =======================================================================
# import {module}
# ... {develop}


# CONSTANTS
# ***********************************************************************
# define constants in uppercase

FIELDS_BASE = [
    "idbacia",
    "cotrecho",
    "cocursodag",
    "cobacia",
    "nuareacont",
    "nuordemcda",
    "nunivotto1",
    "nunivotto2",
    "nunivotto3",
    "nunivotto4",
    "nunivotto5",
    "nunivotto6",
    "nunivotto",
    "nutrjus",
    "id_uph",
    "id_rhi",
    "is_cerrado",
    "is_zhi",
]

FIELDS_INDEXES_INPUTS = ["t", "s", "g", "c", "n", "v", "slope", "uslek"]

N2 = 60
N1 = 10
V1 = -2
SLOPE_THRESHOLD = 5
USLEK_THRESHOLD = 300

APCAC_LABELS = {
    "cd_apcac": [
        "IAN",
        "IAR",
        "IBN",
        "IBR",
        "ICN",
        "ICR",
        "IXN",
        "IXR",
        "IIAN",
        "IIAR",
        "IIBN",
        "IIBR",
        "IICN",
        "IICR",
        "IIXN",
        "IIXR",
    ],
    "lb_apcac": [
        "Predominância natural, importância extremamente alta, baixo risco",
        "Predominância natural, importância extremamente alta, alto risco",
        "Predominância natural, importância muito alta, baixo risco",
        "Predominância natural, importância muito alta, alto risco",
        "Predominância natural, importância alta, baixo risco",
        "Predominância natural, importância alta, alto risco",
        "Predominância natural, importância regular, baixo risco",
        "Predominância natural, importância regular, alto risco",
        "Predominância antrópica, importância extremamente alta, baixo risco",
        "Predominância antrópica, importância extremamente alta, alto risco",
        "Predominância antrópica, importância muito alta, baixo risco",
        "Predominância antrópica, importância muito alta, alto risco",
        "Predominância antrópica, importância alta, baixo risco",
        "Predominância antrópica, importância alta, alto risco",
        "Predominância antrópica, importância regular, baixo risco",
        "Predominância antrópica, importância regular, alto risco",
    ],
}


# FUNCTIONS
# ***********************************************************************

# FUNCTIONS -- Large processes
# =======================================================================


def analysis_apcac(
    input_db,
    raster_files,
    output_folder,
    input_layer="apcac_bho5k",
    raster_multipliers=None,
    cleanup=True,
):
    """
    Orchestrates the complete APCAC (Áreas Prioritárias para Conservação de Água) analysis workflow,
    from sampling raster indexes to generating the final classification GeoPackage, summary CSV, and LaTeX table.

    :param input_db: Path to the initial GeoPackage or database file containing the input vector layer (e.g., catchment polygons).
    :type input_db: str
    :param raster_files: Dictionary where keys are the desired index names and values are the full paths to the corresponding raster files to be sampled.
    :type raster_files: dict
    :param output_folder: Path to the main directory where the final and temporary results will be organized.
    :type output_folder: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :param raster_multipliers: [optional] Dictionary of factors to divide the sampled raster mean values by (used for unit conversion).
    :type raster_multipliers: dict
    :param cleanup: Flag to indicate whether the intermediate, run-specific folders created during the workflow should be deleted. Default value = True
    :type cleanup: bool
    :return: The file path to the final GeoPackage file containing the complete APCAC classification results.
    :rtype: str

    **Notes**

    The function executes the following steps in sequence: sampling raster values, fuzzifying indexes,
    computing index ``a`` (hydrology), computing index ``e`` (erosion risk), calculating the final APCAC
    classification, computing summary statistics, and finally generating the LaTeX table.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        # setup module with importlib
        # ----------------------------------------
        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = "path/to/data.gpkg"

        # define the paths to input rasters
        # ----------------------------------------
        raster_files = {
            # change this paths
            "t": "path/to/raster_t.tif", # topography layer
            "s": "path/to/raster_s.tif", # soil/pedology layer
            "g": "path/to/raster_g.tif", # geology/aquifers layer
            "c": "path/to/raster_c.tif", # climate layer
            "n": "path/to/raster_n.tif", # conservation layer
            "v": "path/to/raster_v.tif", # anthropic risk layer
            "slope": "path/to/raster_slope.tif", # terrain slope layer
            "uslek": "path/to/raster_uslex.tif", # erodibility layer
        }

        # define which index has multipliers (the value is divided)
        # ----------------------------------------
        raster_multipliers = {
            "t": 1000,
            "s": 100,
            "slope": 100,
            # change and add more if needed
        }

        # call the function
        # ----------------------------------------
        module.analysis_apcac(
            input_db=input_db,
            input_layer="apcac_bho5k",
            raster_files=raster_files,
            output_folder=output_dir,
            raster_multipliers=raster_multipliers ,
            cleanup=True
        )


    """

    # Startup
    # -------------------------------------------------------------------
    func_name = analysis_apcac.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # Run processes
    # -------------------------------------------------------------------

    # -----------------------------------
    f1 = sample_indexes(
        output_folder=output_folder,
        input_db=input_db,
        raster_files=raster_files,
        input_layer=input_layer,
        raster_multipliers=raster_multipliers,
    )

    # -----------------------------------
    f2 = fuzzify_indexes(
        input_db=f1,
        input_layer=input_layer,
        output_folder=output_folder,
    )
    # -----------------------------------
    f3 = compute_index_a(
        input_db=f2,
        input_layer=input_layer,
        output_folder=output_folder,
    )

    # -----------------------------------
    f4 = compute_index_e(
        input_db=f3,
        input_layer=input_layer,
        output_folder=output_folder,
        uslek_threshold=4500,
    )

    # -----------------------------------
    f_apcac = compute_apcac(
        input_db=f4,
        input_layer=input_layer,
        output_folder=output_folder,
    )
    # -----------------------------------
    f_stats = compute_apcac_stats(
        input_db=f_apcac,
        input_layer=input_layer,
        output_folder=output_folder,
    )
    # -----------------------------------
    f_latex = get_latex_table(
        input_csv=f_stats,
        output_folder=output_folder,
    )

    # Export
    # -------------------------------------------------------------------

    # copy files
    # -----------------------------------
    shutil.copy(
        src=f_apcac,
        dst=output_file,
    )
    shutil.copy(
        src=f_stats,
        dst=str(output_file).replace(".gpkg", ".csv"),
    )
    shutil.copy(
        src=f_latex,
        dst=str(output_file).replace(".gpkg", ".tex"),
    )

    # delete intermediate files
    # -----------------------------------
    if cleanup:
        ls_removals = [f1, f2, f3, f4, f_apcac, f_stats, f_latex]
        for f in ls_removals:
            d = Path(f).parent
            shutil.rmtree(d)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def analysis_apcac_upscaled(
    input_db,
    output_folder,
    input_layer="apcac_bho5k",
    field_upscale=None,
    field_area=None,
    cleanup=True,
):
    """
    Orchestrates the complete APCAC analysis workflow at an upscaled (aggregated)
    spatial unit, performing area-weighted aggregation of indexes
    before calculating the final APCAC classification.


    :param input_db: Path to the GeoPackage or database file containing the **fine-resolution** input vector layer.
    :type input_db: str
    :param output_folder: Path to the main directory where the final and temporary results will be organized.
    :type output_folder: str
    :param input_layer: Name of the vector layer within the input database (fine-resolution) to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :param field_upscale: [optional] The column name in the input data to use for grouping/dissolving (the ID of the coarser unit). Default value = "nunivotto5"
    :type field_upscale: str
    :param field_area: [optional] The column name representing the area of the features, used for weighted averaging. Default value = None
    :type field_area: str
    :param cleanup: Flag to indicate whether the intermediate, run-specific folders created during the workflow should be deleted. Default value = True
    :type cleanup: bool
    :return: The file path to the final GeoPackage file, which contains the complete APCAC classification results for the upscaled spatial units.
    :rtype: str

    **Notes**

    The function first computes the upscaled indexes and
    geometries using ``compute_upscaled_indexes``, then proceeds with the
    standard steps: fuzzifying indexes, computing index 'a' (hydrology),
    computing index 'e' (erosion risk), calculating the final
    APCAC classification for the upscaled units, computing summary statistics,
    and finally generating the LaTeX table.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        # setup module with importlib
        # ----------------------------------------
        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = "path/to/data.gpkg"

        # call the function
        # ----------------------------------------
        output_file = module.analysis_apcac_upscaled(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
            field_upscale="nunivotto4"
        )


    """

    # Startup
    # -------------------------------------------------------------------
    func_name = analysis_apcac_upscaled.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------
    if field_upscale is None:
        field_upscale = "nunivotto5"

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # Run processes
    # -------------------------------------------------------------------

    # -----------------------------------
    f1 = compute_upscaled_indexes(
        input_db=input_db,
        input_layer=input_layer,
        output_folder=output_folder,
        field_upscale=field_upscale,
        field_area=field_area,
    )

    # -----------------------------------
    f2 = fuzzify_indexes(
        input_db=f1,
        input_layer=f"apcac_{field_upscale}",
        output_folder=output_folder,
    )
    # -----------------------------------
    f3 = compute_index_a(
        input_db=f2,
        input_layer=f"apcac_{field_upscale}",
        output_folder=output_folder,
    )

    # -----------------------------------
    f4 = compute_index_e(
        input_db=f3,
        input_layer=f"apcac_{field_upscale}",
        output_folder=output_folder,
        uslek_threshold=4500,
    )

    # -----------------------------------
    f_apcac = compute_apcac(
        input_db=f4,
        input_layer=f"apcac_{field_upscale}",
        output_folder=output_folder,
    )
    # -----------------------------------
    f_stats = compute_apcac_stats(
        input_db=f_apcac,
        input_layer=f"apcac_{field_upscale}",
        output_folder=output_folder,
    )
    # -----------------------------------
    f_latex = get_latex_table(
        input_csv=f_stats,
        output_folder=output_folder,
    )

    # Export
    # -------------------------------------------------------------------

    # copy files
    # -----------------------------------
    shutil.copy(
        src=f_apcac,
        dst=output_file,
    )
    shutil.copy(
        src=f_stats,
        dst=str(output_file).replace(".gpkg", ".csv"),
    )
    shutil.copy(
        src=f_latex,
        dst=str(output_file).replace(".gpkg", ".tex"),
    )

    # delete intermediate files
    # -----------------------------------
    if cleanup:
        ls_removals = [f1, f2, f3, f4, f_apcac, f_stats, f_latex]
        for f in ls_removals:
            d = Path(f).parent
            shutil.rmtree(d)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


# FUNCTIONS -- Project-level
# =======================================================================


def sample_indexes(
    output_folder,
    input_db,
    raster_files,
    input_layer="apcac_bho5k",
    raster_multipliers=None,
):
    """
    Samples mean values from multiple raster files over a vector layer
    (e.g., catchments) and merges the results into a GeoDataFrame.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer.
    :type input_db: str
    :param raster_files: Dictionary where keys are the desired column names (index names) and values are the full paths to the corresponding raster files.
    :type raster_files: dict
    :param input_layer: Name of the vector layer within the input database to use for zonal statistics. Default value = "apcac_bho5k"
    :type input_layer: str
    :param raster_multipliers: [optional] Dictionary where keys are the index names (from ``raster_files``) and values are factors by which the sampled mean values should be divided (e.g., to convert units).
    :type raster_multipliers: dict
    :return: The file path to the final GeoPackage file containing the input layer with the new sampled index columns.
    :rtype: str

    **Notes**

    The process uses QGIS's native zonal statistics algorithm (``native:zonalstatisticsfb``)
    to calculate the mean of each raster within the polygons of the input vector layer.


    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"

        # define the paths to input rasters
        # ----------------------------------------
        raster_files = {
            # change this paths
            "t": f"{input_dir}/path/to/raster_t.tif",
            "s": f"{input_dir}/path/to/raster_s.tif",
            "g": f"{input_dir}/path/to/raster_g.tif",
            "c": f"{input_dir}/path/to/raster_c.tif",
            "n": f"{input_dir}/path/to/raster_n.tif",
            "v": f"{input_dir}/path/to/raster_v.tif",
            "slope": f"{input_dir}/path/to/raster_slope.tif",
            "uslek": f"{input_dir}/path/to/raster_uslek.tif",
        }

        # define which index has multipliers (the value is divided)
        # ----------------------------------------
        raster_multipliers = {
            "t": 1000,
            "s": 100,
            "slope": 100,
            # change and add more if needed
        }

        # call the function
        # ----------------------------------------
        module.sample_indexes(
            input_db=input_db,
            raster_files=raster_files,
            output_folder=output_dir,
            raster_multipliers=raster_multipliers,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = sample_indexes.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------
    ls_input_indexes = []

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # Run processes
    # -------------------------------------------------------------------

    # sampling loop
    # -----------------------------------
    for index in raster_files:
        index_name = index[:]
        index_file = raster_files[index]
        print(f">> sampling {index_name} from \n {index_file}")

        processing.run(
            "native:zonalstatisticsfb",
            {
                "INPUT": "{}|layername={}".format(input_db, input_layer),
                "INPUT_RASTER": index_file,
                "RASTER_BAND": 1,
                "COLUMN_PREFIX": f"{index_name}_",
                "STATISTICS": [2],
                "OUTPUT": "ogr:dbname='{}' table=\"{}\" (geom)".format(
                    output_file, index_name
                ),
            },
        )
        ls_input_indexes.append(index_name)

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)
    gdf = gdf[FIELDS_BASE + ["geometry"]].copy()

    # organization loop
    # -----------------------------------
    for index in ls_input_indexes:
        gdf_index = gpd.read_file(output_file, layer=index)
        gdf_index = gdf_index[["cobacia", f"{index}_mean"]].copy()
        gdf_index.rename(columns={f"{index}_mean": index}, inplace=True)
        gdf = pd.merge(left=gdf, right=gdf_index, on="cobacia", how="left")

    # handle optional multipliers
    # -----------------------------------
    if raster_multipliers is not None:
        for index in raster_multipliers:
            gdf[index] = gdf[index] / raster_multipliers[index]

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    os.remove(output_file)
    save_gdf(gdf, db=output_file, layer=input_layer)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def fuzzify_indexes(output_folder, input_db, input_layer="apcac_bho5k"):
    """
    Applies a fuzzification function to a predefined list of index columns
    in a GeoDataFrame, scaling their values between 0 and 1.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer.
    :type input_db: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :return: The file path to the final GeoPackage file, which contains the input layer with the new fuzzified index columns (e.g., ``t_f``, ``s_f``).
    :rtype: str

    **Notes**

    The fuzzification is typically a linear scaling based on the minimum
    and maximum values observed in each column.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"


        # call the function
        # ----------------------------------------
        output_file = module.fuzzify_indexes(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = fuzzify_indexes.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------
    ls_fields = ["t", "s", "g", "c", "n", "v", "slope", "uslek"]

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # fuzzify fields
    # -----------------------------------
    for field in ls_fields:
        field_lo = gdf[field].min()
        field_up = gdf[field].max()
        field_name_fuzzy = f"{field}_f"
        gdf[field_name_fuzzy] = fuzzify(gdf[field].values, field_lo, field_up)

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    save_gdf(gdf, db=output_file, layer=input_layer)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_index_a(output_folder, input_db, input_layer="apcac_bho5k"):
    """
    Computes the raw and fuzzified ``a`` (hydrology importance) index as
    a multiplicative combination of the fuzzified ``t``, ``s``, ``g``, and ``c`` indexes.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer.
    :type input_db: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :return: The file path to the final GeoPackage file, which contains the input layer with the new ``a_raw`` and fuzzified ``a`` columns.
    :rtype: str

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"


        # call the function
        # ----------------------------------------
        output_file = module.compute_index_a(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_a.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # compute a raw
    # -----------------------------------
    gdf["a_raw"] = gdf["t_f"] * gdf["s_f"] * gdf["g_f"] * gdf["c_f"]

    # fuzzify a
    # -----------------------------------
    a_lo = gdf["a_raw"].min()
    a_up = gdf["a_raw"].max()
    gdf["a"] = fuzzify(gdf["a_raw"].values, a_lo, a_up)

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    save_gdf(gdf, db=output_file, layer=input_layer)
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_index_e(
    output_folder,
    input_db,
    input_layer="apcac_bho5k",
    n_threshold=None,
    slope_threshold=None,
    uslek_threshold=None,
):
    """
    Computes the binary ``e`` (erosion/degradation risk) index, classifying areas
    as having risk (1) if they meet at least one of the three predefined risk
    conditions: low ``n``, high ``slope``, or high ``uslek``.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer.
    :type input_db: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type n_threshold: [optional] The maximum ``n`` value (vegetation index) considered to indicate risk. Default value = N1
    :type n_threshold: float
    :param slope_threshold: [optional] The minimum ``slope`` value considered to indicate risk. Default value = SLOPE_THRESHOLD
    :type slope_threshold: float
    :param uslek_threshold: [optional] The minimum ``uslek`` value (soil erodibility) considered to indicate risk. Default value = USLEK_THRESHOLD
    :type uslek_threshold: float
    :return: The file path to the final GeoPackage file, which contains the input layer with the new boolean risk columns (``is_risk_n``, ``is_risk_slope``, ``is_risk_uslek``) and the final ``e`` index.
    :rtype: str


    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"


        # call the function
        # ----------------------------------------
        output_file = module.compute_index_e(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_e.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    if n_threshold is None:
        n_threshold = N1

    if slope_threshold is None:
        slope_threshold = SLOPE_THRESHOLD

    if uslek_threshold is None:
        uslek_threshold = USLEK_THRESHOLD

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # compute boolean risk factors
    # -----------------------------------
    gdf["is_risk_n"] = np.where(gdf["n"].values <= n_threshold, 1, 0)
    gdf["is_risk_slope"] = np.where(gdf["slope"].values >= slope_threshold, 1, 0)
    gdf["is_risk_uslek"] = np.where(gdf["uslek"].values >= uslek_threshold, 1, 0)

    # classify risk
    # -----------------------------------
    # gdf["e"] = gdf["is_risk_n"] * gdf["is_risk_slope"] * gdf["is_risk_uslek"]
    gdf["e"] = gdf["is_risk_n"] + gdf["is_risk_slope"] + gdf["is_risk_uslek"]
    gdf["e"] = np.where(gdf["e"].values > 0, 1, 0)

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    save_gdf(gdf, db=output_file, layer=input_layer)
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_upscaled_indexes(
    output_folder,
    input_db,
    field_upscale=None,
    input_layer="apcac_bho5k",
    field_area=None,
):
    """
    Computes area-weighted upscaled (aggregated) values for various
    indexes and boolean flags from a fine-resolution GeoDataFrame to
    a coarser spatial unit defined by a grouping field, and
    saves the results as a new GeoPackage layer.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer (fine-resolution catchments).
    :type input_db: str
    :param field_upscale: [optional] The column name in the input data to use for grouping/dissolving (the ID of the coarser unit). Default value = "nunivotto5"
    :type field_upscale: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :param field_area: [optional] The column name representing the area of the features, used for weighted averaging. Default value = "nuareacont"
    :type field_area: str
    :return: The file path to the final GeoPackage file, which contains the upscaled indexes merged with the dissolved geometries of the coarser spatial units.
    :rtype: str

    **Notes**

    The function first calculates the upscaled values using ``upscale_indexes``,
    then dissolves the geometries based on the grouping field, and finally
    merges the upscaled data with the dissolved geometries.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        # setup module with importlib
        # ----------------------------------------
        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = "path/to/data.gpkg"

        # call the function
        # ----------------------------------------
        output_file = module.compute_upscaled_indexes(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
            field_upscale="nunivotto4",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_upscaled_indexes.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------
    if field_upscale is None:
        field_upscale = "nunivotto5"

    if field_area is None:
        field_area = "nuareacont"

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/indexes_upscaled_{field_upscale}.gpkg")

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # upscale info
    # -----------------------------------
    df_up = upscale_indexes(gdf=gdf, field_upscale=field_upscale, field_area=field_area)

    # dissolve geometries
    # -----------------------------------
    processing.run(
        "native:dissolve",
        {
            "INPUT": f"{input_db}|layername={input_layer}",
            "FIELD": [field_upscale],
            "SEPARATE_DISJOINT": False,
            "OUTPUT": "ogr:dbname='{}' table=\"apcac_{}\" (geom)".format(
                output_file, field_upscale
            ),
        },
    )

    # load dissolved data
    # -----------------------------------
    gdf_up = gpd.read_file(output_file, layer=f"apcac_{field_upscale}")
    gdf_up = gdf_up[[field_upscale, "geometry"]]

    # merge
    # -----------------------------------
    gdf_up = pd.merge(left=gdf_up, right=df_up, on=field_upscale, how="left")

    # Export
    # -------------------------------------------------------------------
    save_gdf(gdf_up, output_file, layer=f"apcac_{field_upscale}")
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_apcac(output_folder, input_db, input_layer="apcac_bho5k"):
    """
    Calculates the final APCAC (Áreas Prioritárias para Conservação de Água)
    classification codes and IDs for the input catchment GeoDataFrame.

    :param output_folder: Path to the directory where temporary and final output files will be stored.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the input vector layer with all required index columns.
    :type input_db: str
    :param input_layer: Name of the vector layer within the input database to be processed. Default value = "apcac_bho5k"
    :type input_layer: str
    :return: The file path to the final GeoPackage file, which contains the input layer with the full set of APCAC classification columns (``cd_apcac``, ``id_apcac``, and their component parts).
    :rtype: str

    **Notes**

    This function wraps the three-level classification logic
    (natural/anthropic, hydrology, and risk) defined in ``classify_apcac``.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"


        # call the function
        # ----------------------------------------
        output_file = module.compute_apcac(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_apcac.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac.gpkg")

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # compute apcac
    # -----------------------------------
    gdf = classify_apcac(gdf)

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    save_gdf(gdf, db=output_file, layer=input_layer)
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_apcac_stats(output_folder, input_db, input_layer="apcac_bho5k"):
    """
    Computes and exports a summary of APCAC classification statistics,
    including total area and percentages for the Biome (Cerrado)
    and the Hydrological Influence Zone (ZHI).

    :param output_folder: Path to the directory where the output CSV file will be saved.
    :type output_folder: str
    :param input_db: Path to the GeoPackage or database file containing the classified vector layer.
    :type input_db: str
    :param input_layer: Name of the vector layer within the input database to be processed, which must contain the ``cd_apcac`` column. Default value = "apcac_bho5k"
    :type input_layer: str
    :return: The file path to the resulting CSV file containing the APCAC summary statistics.
    :rtype: str

    **Notes**

    This function loads the classified catchment data, calls the `summarise`
    function to aggregate the statistics, and saves the resulting table to a CSV file.

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input database
        # ----------------------------------------
        input_db = f"{input_dir}/path/to/data.gpkg"


        # call the function
        # ----------------------------------------
        output_file = module.compute_apcac_stats(
            input_db=input_db,
            output_folder=output_dir,
            input_layer="apcac_bho5k",
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_apcac_stats.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac_stats.csv")

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=input_layer)

    # compute apcac stats
    # -----------------------------------
    df = summarise(gdf)

    # Export
    # -------------------------------------------------------------------

    # save data
    # -----------------------------------
    df.to_csv(output_file, sep=";", index=False)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def get_latex_table(output_folder, input_csv):
    """
    Reads a CSV file containing APCAC summary statistics, converts
    the data into a fully formatted LaTeX table using `summarise_latex`,
    and saves the resulting LaTeX code to a .tex file.

    :param output_folder: Path to the directory where the output LaTeX file will be saved.
    :type output_folder: str
    :param input_csv: Path to the input CSV file containing the APCAC summary statistics (e.g., the output of `compute_apcac_stats`).
    :type input_csv: str
    :return: The file path to the resulting LaTeX (.tex) file containing the formatted APCAC summary table.
    :rtype: str

    **Script example**

    .. code-block:: python

        import importlib.util as iu

        # define the paths to this module
        # ----------------------------------------
        the_module = "path/to/classes.py"

        spec = iu.spec_from_file_location("module", the_module)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

        # define the paths to input and output folders
        # ----------------------------------------
        input_dir = "path/to/input_folder"
        output_dir = "path/to/output_folder"

        # define the path to input data
        # ----------------------------------------
        input_file = f"{input_dir}/path/to/data.csv"

        # call the function
        # ----------------------------------------
        output_file = module.get_latex_table(
            input_csv=input_file,
            output_folder=output_dir,
        )

    """

    # Startup
    # -------------------------------------------------------------------
    func_name = get_latex_table.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(run_name=func_name, output_folder=output_folder)

    # files
    # -----------------------------------
    output_file = Path(f"{output_folder}/apcac_stats.tex")

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    df = pd.read_csv(input_csv, sep=";")

    # convert to LaTeX table
    # -----------------------------------
    s_table = summarise_latex(df)

    # Export
    # -------------------------------------------------------------------

    # save table
    # -----------------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(s_table)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


# ... {develop}


# FUNCTIONS -- Module-level
# =======================================================================


def save_gdf(gdf, db, layer):
    """
    Saves a GeoDataFrame to a GeoPackage file, ensuring the
    ``geometry`` column is the last column.

    :param gdf: The GeoDataFrame to be saved.
    :type gdf: :class:`geopandas.GeoDataFrame`
    :param db: The file path for the output GeoPackage database.
    :type db: str or :class:`pathlib.Path`
    :param layer: The name of the layer (table) to create within the GeoPackage.
    :type layer: str

    **Notes**

    The function first reorders the GeoDataFrame columns to
    place the ``geometry``  column at the end, which is a common
    convention or requirement for some geospatial operations,
    and then writes the data to the specified GeoPackage file.

    """
    # organize columns
    my_list = list(gdf.columns)
    item = my_list.pop(my_list.index("geometry"))  # remove and get the item
    my_list.append(item)
    gdf = gdf[my_list].copy()
    print(" >> saving...")
    gdf.to_file(db, layer=layer, driver="GPKG")
    return None


def classify_apcac(gdf):
    """
    Classifies catchments based on natural/anthropic,
    hydrology, and risk factors using a three-level system (APCAC).

    :param gdf: GeoDataFrame containing catchment data with ``n``, ``a``, ``v``, and ``e`` columns for classification.
    :type gdf: :class:`geopandas.GeoDataFrame`
    :return: GeoDataFrame with added classification columns: ``cd_apcac_n``, ``id_apcac_n``, ``cd_apcac_a``, ``id_apcac_a``, ``cd_apcac_risk``, ``id_apcac_risk``, ``cd_apcac``, and ``id_apcac``.
    :rtype: :class:`geopandas.GeoDataFrame`
    """

    # level 1 -- natural or anthropic
    # -------------------------------------------------------------------
    gdf["cd_apcac_n"] = np.where(gdf["n"] >= N2, "I", "II")
    gdf["id_apcac_n"] = np.where(gdf["n"] >= N2, 100, 200)
    gdf["id_apcac_n"] = gdf["id_apcac_n"].astype(int)

    # level 2 --- hydrology
    # -------------------------------------------------------------------
    gdf["a"] = gdf["a"].fillna(0)
    thresholds = [
        0,
        np.percentile(gdf["a"].values, 40),
        np.percentile(gdf["a"].values, 70),
        np.percentile(gdf["a"].values, 90),
        np.inf,
    ]
    labels = ["X", "C", "B", "A"]
    labels_id = [40, 30, 20, 10]
    # Bin values
    gdf["cd_apcac_a"] = pd.cut(gdf["a"], bins=thresholds, labels=labels, right=False)
    gdf["id_apcac_a"] = pd.cut(gdf["a"], bins=thresholds, labels=labels_id, right=False)
    gdf["id_apcac_a"] = gdf["id_apcac_a"].astype(int)

    # split
    gdf_n = gdf.query("cd_apcac_n == 'I'").copy()
    gdf_a = gdf.query("cd_apcac_n == 'II'").copy()

    # level 3 --- special cases
    # -------------------------------------------------------------------
    # risk in natural catchments
    gdf_n["cd_apcac_risk"] = np.where(gdf_n["v"] <= V1, "R", "N")
    gdf_n["id_apcac_risk"] = np.where(gdf_n["v"] <= V1, 2, 1)
    gdf_n["id_apcac_risk"] = gdf_n["id_apcac_risk"].astype(int)

    # risk in anthropic catchments
    # -------------------------------------------------------------------
    gdf_a["cd_apcac_risk"] = np.where(gdf_a["e"] > 0, "R", "N")
    gdf_a["id_apcac_risk"] = np.where(gdf_a["e"] > 0, 2, 1)

    # wrap up
    # -------------------------------------------------------------------

    # concat
    gdf = pd.concat([gdf_n, gdf_a]).reset_index(drop=True)

    # concat columns
    gdf["cd_apcac"] = (
        gdf["cd_apcac_n"].astype(str)
        + gdf["cd_apcac_a"].astype(str)
        + gdf["cd_apcac_risk"].astype(str)
    )
    gdf["id_apcac"] = (
        gdf["id_apcac_n"].values
        + gdf["id_apcac_a"].values
        + gdf["id_apcac_risk"].values
    )

    return gdf


def upscale_indexes(gdf, field_upscale, field_area):
    """
    Upscales various numeric indexes and boolean flags from a finer-resolution GeoDataFrame to a coarser resolution based on an aggregation field.

    Numeric indexes are upscaled using an area-weighted average, and boolean fields are upscaled to be true (1) if any part of the aggregated unit contains a true value.

    :param gdf: GeoDataFrame containing the fine-resolution data, including all index fields, the aggregation field, and the area field.
    :type gdf: :class:`geopandas.GeoDataFrame`
    :param field_upscale: The column name in `gdf` to use for grouping and upscaling (e.g., a coarser watershed ID).
    :type field_upscale: str
    :param field_area: The column name in `gdf` that represents the area of the features, used for weighted averaging of indexes.
    :type field_area: str
    :return: DataFrame containing the upscaled results, with one row per unique value in `field_upscale`, including the area-weighted mean for each index and the aggregated boolean flags.
    :rtype: :class:`pandas.DataFrame`
    """

    ls_dfs = []

    # indexes loop for upscaling
    # -------------------------------------------------------------------
    for index in FIELDS_INDEXES_INPUTS:
        gdf[f"weighted_{index}"] = gdf[index] * gdf[field_area]
        df_upscaled = (
            gdf.groupby(field_upscale)[[f"weighted_{index}", field_area]]
            .sum()
            .eval(f"{index} = weighted_{index} / {field_area}")
            .reset_index()[[field_upscale, index]]
        )
        ls_dfs.append(df_upscaled.copy())

    # area
    # -------------------------------------------------------------------
    df_area = gdf.groupby(field_upscale)[field_area].sum().reset_index()
    # df_area.rename(columns={field_area: }, inplace=True)
    ls_dfs.append(df_area)

    # booleans loop
    # -------------------------------------------------------------------
    bool_fields = ["is_cerrado", "is_zhi"]
    df_bool = gdf.groupby(field_upscale)[bool_fields].sum()
    df_bool = (df_bool > 0).astype(int).reset_index()
    dc = {
        "is_cerrado_sum": "is_cerrado",
        "is_zhi_sum": "is_zhi",
    }
    # df_bool.rename(columns=dc, inplace=True)
    ls_dfs.append(df_bool)

    # merger loop
    # -------------------------------------------------------------------
    df_output = ls_dfs[0]
    for df in ls_dfs[1:]:
        df_output = pd.merge(df_output, df, on=field_upscale, how="left")

    return df_output


def groupby(gdf, label, value, rename):
    """
    Groups a GeoDataFrame by a specified label, aggregates a value
    column by summing, and calculates the percentage of the total for the summed value.

    :param gdf: GeoDataFrame to be processed.
    :type gdf: :class:`geopandas.GeoDataFrame`
    :param label: Column name to use for grouping (the index of the resulting DataFrame).
    :type label: str
    :param value: Column name to be summed within each group.
    :type value: str
    :param rename: Base name for the new columns created for the summed value and its percentage.
    :type rename: str
    :return: DataFrame with the grouped label, the sum of the value column (renamed), and the percentage of the total sum (renamed with ``_p`` suffix).
    :rtype: :class:`pandas.DataFrame`
    """
    gdf_ups = gdf.groupby(label)[value].agg(["sum"]).reset_index()
    gdf_ups = gdf_ups.rename(columns={"sum": rename})
    gdf_ups[f"{rename}_p"] = 100 * gdf_ups[rename] / gdf_ups[rename].sum()
    gdf_ups[f"{rename}_p"] = gdf_ups[f"{rename}_p"].round(2)
    gdf_ups[rename] = gdf_ups[rename].round(0)
    return gdf_ups


def summarise(gdf):
    """
    Summarizes catchment data by calculating the total area and percentage
    of area for each APCAC classification, both for a specific biome (Cerrado)
    and for the full dataset.

    :param gdf: GeoDataFrame containing catchment data with required columns ``id_uph``, ``is_cerrado``, ``nuareacont``, and ``cd_apcac``.
    :type gdf: :class:`geopandas.GeoDataFrame`
    :return: DataFrame with APCAC labels, the total area (in km²) and percentage of area for each classification within the Cerrado biome, and the total area and percentage for the full extent.
    :rtype: :class:`pandas.DataFrame`
    """
    gdf_labels = pd.DataFrame(APCAC_LABELS)

    # filter fields
    # -------------------------------------------------------------------
    gdf = gdf[["is_cerrado", "nuareacont", "cd_apcac"]].copy()

    # run biome scale analysis
    # -------------------------------------------------------------------
    gdf_main_cerrado = gdf.query("is_cerrado == 1")
    gdf_grouped_bio = groupby(
        gdf=gdf_main_cerrado,
        label="cd_apcac",
        value="nuareacont",
        rename="bio_area_km2",
    )

    # run full scale analysis
    # -------------------------------------------------------------------
    gdf_grouped_zhi = groupby(
        gdf=gdf, label="cd_apcac", value="nuareacont", rename="zhi_area_km2"
    )

    # merges
    # -------------------------------------------------------------------
    gdf_output = pd.merge(
        left=gdf_grouped_bio, right=gdf_grouped_zhi, on="cd_apcac", how="left"
    )

    gdf_output = pd.merge(left=gdf_labels, right=gdf_output, on="cd_apcac", how="left")
    gdf_output = gdf_output.fillna(0)

    return gdf_output


def summarise_latex(df):
    """
    Generates a full LaTeX table environment, including caption and formatting,
    from a summary DataFrame of APCAC classifications.

    :param df: DataFrame containing APCAC summary results, including ``cd_apcac``, ``lb_apcac``, ``bio_area_km2``, ``bio_area_km2_p``, ``zhi_area_km2``, and ``zhi_area_km2_p`` columns.
    :type df: :class:`pandas.DataFrame`
    :return: A string containing the complete LaTeX code for the formatted table.
    :rtype: str

    **Notes**

    The table organizes data by ``Importância Hidrológica`` (Hydrological Importance)
    with subtotals and includes ``Risco`` (Risk) and ``Ocupação`` (Occupation), showing
    area (km²) and percentage for both the Biome (Cerrado) and the Hydrological Influence Zone (ZHI).

    """
    # Map keywords to importance levels in Portuguese
    importance_map = {
        "extremamente alta": "Extremamente alta",
        "muito alta": "Muito alta",
        "alta": "Alta",
        "regular": "Regular",
    }

    # Parse the descriptive column to extract occupation, importance, and risk
    def parse_description(desc):
        parts = desc.split(", ")
        occupation = "Antrópica" if "antrópica" in parts[0] else "Natural"
        importance = next(
            (importance_map[k] for k in importance_map if k in parts[1]), None
        )
        risk = "Alto" if "alto risco" in parts[-1] else "Baixo"
        return occupation, importance, risk

    df[["Ocupação", "Importância Hidrológica", "Risco"]] = df["lb_apcac"].apply(
        lambda x: pd.Series(parse_description(x))
    )

    # Sort by importance order
    importance_order = ["Extremamente alta", "Muito alta", "Alta", "Regular"]
    df["order"] = df["Importância Hidrológica"].apply(
        lambda x: importance_order.index(x)
    )
    df = df.sort_values(["order", "Ocupação", "Risco"]).reset_index(drop=True)

    # Format numbers for Brazilian style
    def fmt(x):
        return f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_p(x):
        return f"{x:.2f}".replace(".", ",")

    # Compute totals per importance group
    totals = (
        df.groupby("Importância Hidrológica")[
            ["bio_area_km2", "bio_area_km2_p", "zhi_area_km2", "zhi_area_km2_p"]
        ]
        .sum()
        .reset_index()
    )
    grand_total = df[
        ["bio_area_km2", "bio_area_km2_p", "zhi_area_km2", "zhi_area_km2_p"]
    ].sum()

    # Start LaTeX table construction
    lines = []
    lines.append("\\begin{tabular}{llllrrrr}")
    lines.append("\\toprule")
    lines.append(
        "\\textbf{Classe} & \\textbf{Importância Hidrológica} & \\textbf{Risco} & \\textbf{Ocupação} & "
        "\\textbf{Bioma (km²)} & \\textbf{Bioma (\\%)} & \\textbf{ZHI (km²)} & \\textbf{ZHI (\\%)} \\\\"
    )
    lines.append("\\midrule")

    # Iterate over importance groups
    for imp in importance_order:
        sub = df[df["Importância Hidrológica"] == imp]
        total = totals.loc[totals["Importância Hidrológica"] == imp].iloc[0]

        # Subtotal line for each importance group
        lines.append(
            f"     & \\textbf{{{imp}}} & & & "
            f"\\textbf{{{fmt(total.bio_area_km2)}}} & \\textbf{{{fmt_p(total.bio_area_km2_p)}}} & "
            f"\\textbf{{{fmt(total.zhi_area_km2)}}} & \\textbf{{{fmt_p(total.zhi_area_km2_p)}}} \\\\"
        )

        # Detailed rows
        for _, row in sub.iterrows():
            lines.append(
                f"{row.cd_apcac} & {row['Importância Hidrológica']} & {row.Risco} & {row.Ocupação} & "
                f"{fmt(row.bio_area_km2)} & {fmt_p(row.bio_area_km2_p)} & "
                f"{fmt(row.zhi_area_km2)} & {fmt_p(row.zhi_area_km2_p)} \\\\"
            )

        lines.append("\\midrule")

    # Final total line
    lines.append(
        f"\\textbf{{Total}} & & & & \\textbf{{{fmt(grand_total.bio_area_km2)}}} & "
        f"\\textbf{{100}} & \\textbf{{{fmt(grand_total.zhi_area_km2)}}} & \\textbf{{100}} \\\\"
    )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")

    tabular = "\n".join(lines)

    # === Wrap inside a full table environment ===
    latex_table = f"""
% start the table
\\begin{{table}}[h!] % placed on top of page
\\centering   
\\scriptsize % table font size
\\sffamily % table font style
\\caption[Resultados na malha BHO]{{
Resultados da classificação de áreas prioritárias para a conservação de água na malha de bacias hidrográficas da BHO5k. 
Resumo dos percentuais de área e de classes obtidas, com agregação no âmbito do Bioma Cerrado e da Zona de Influência Hidrológica (ZHI) — 
definida como o conjunto de bacias hidrográficas que intersectam o Cerrado.
}}
\\label{{tbl:results}}
% set alternating colors
\\rowcolors{{2}}{{white}}{{rowgray}}
% start the tabular environment
\\centering

{tabular}

\\end{{table}}
    """

    # Remove indentation from the triple-quoted string
    latex_table = textwrap.dedent(latex_table)

    return latex_table


# FUNCTIONS -- Utils
# =======================================================================


def get_timestamp():
    now = datetime.datetime.now()
    return str(now.strftime("%Y-%m-%dT%H%M%S"))


def make_run_folder(output_folder, run_name):
    """
    Creates a unique, time-stamped run folder within a specified output directory.

    :param output_folder: The parent directory where the new run folder will be created.
    :type output_folder: str or :class:`pathlib.Path`
    :param run_name: The base name for the new folder. A timestamp will be appended to it.
    :type run_name: str
    :return: The absolute path to the newly created run folder.
    :rtype: str

    **Notes**

    It appends a unique timestamp to the run name and ensures the
    folder doesn't already exist before creating it.

    """
    while True:
        ts = get_timestamp()
        folder_run = Path(output_folder) / f"{run_name}_{ts}"
        if os.path.exists(folder_run):
            time.sleep(1)
        else:
            os.mkdir(folder_run)
            break

    return os.path.abspath(folder_run)


def fuzzify(v, v_lo, v_up):
    """
    Fuzzifies an array using a trapezoidal membership function, limiting values outside the bounds.

    :param v: The input array of values to fuzzify.
    :type v: :class:`numpy.ndarray`
    :param v_lo: The lower bound for the trapezoidal function's base. Values below this will have a membership of 0.
    :type v_lo: float
    :param v_up: The upper bound for the trapezoidal function's base. Values above this will have a membership of 0.
    :type v_up: float
    :return: The fuzzified array, with membership degrees between 0 and 1.
    :rtype: :class:`numpy.ndarray`

    **Notes**

    This function first applies linear scaling (min-max normalization)
     to the values and then sets the membership degree to 0 for any value strictly outside the given bounds.

    """
    # apply function
    v_f = fuzzify_linear(v, v_lo, v_up)
    # get bounds
    v_lo_bool = np.where(v < v_lo, 0, 1)
    v_up_bool = np.where(v > v_up, 0, 1)
    # return boolean product
    return v_f * v_lo_bool * v_up_bool


def fuzzify_linear(v, v_lo=None, v_up=None):
    """
    Briefly fuzzifies a linear array using min-max scaling.


    :param v: The input array of values to fuzzify.
    :type v: :class:`numpy.ndarray`
    :param v_lo: [optional] The lower bound for scaling (0.0). If None, the minimum non-NaN value of `v` is used.
    :type v_lo: float or None
    :param v_up: [optional] The upper bound for scaling (1.0). If None, the maximum non-NaN value of `v` is used.
    :type v_up: float or None
    :return: The fuzzified array, scaled between 0 and 1.
    :rtype: :class:`numpy.ndarray`

    **Notes**

    The array is scaled between 0 and 1 using the provided lower
    and upper bounds. If both bounds are equal, 1.0 is returned for non-NaN values.

    """
    v = np.asarray(v, dtype=float)
    if v_lo is None:
        v_lo = np.nanmin(v)
    if v_up is None:
        v_up = np.nanmax(v)

    if v_lo == v_up:
        # If all valid values are equal, return 1.0 where not NaN
        return np.where(np.isnan(v), np.nan, 1.0)

    return (v - v_lo) / (v_up - v_lo)


# ... {develop}


# SCRIPT
# ***********************************************************************
# standalone behaviour as a script
if __name__ == "__main__":

    print("Hello World")
