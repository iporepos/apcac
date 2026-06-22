# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2025 The Project Authors
# See pyproject.toml for authors/maintainers.
# See LICENSE for license details.
"""
{Short module description (1-3 sentences)}
todo docstring

Features
--------
todo docstring

* {feature 1}
* {feature 2}
* {feature 3}
* {etc}

Overview
--------
todo docstring
{Overview description}

Examples
--------
todo docstring
{Examples in rST}

Print a message

.. code-block:: python

    # print message
    print("Hello world!")
    # [Output] >> 'Hello world!'


"""

# IMPORTS
# ***********************************************************************
# import modules from other libs

# Native imports
# =======================================================================
import os, shutil
import time, datetime
from pathlib import Path

# ... {develop}

# External imports
# =======================================================================
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
# Fields carried through from the source BHO layer into every output
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

# FUNCTIONS
# ***********************************************************************

# FUNCTIONS -- Project-level
# =======================================================================


def compute_index_e(input_slope, input_k, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_e.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_v(input_n0, input_n1, t0, t1, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_v.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_n(input_ppt, input_pet, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_n.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_c(input_ppt, input_pet, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_c.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_g(input_q, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_g.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_s(input_sandp, input_socp, output_folder):
    # todo docstring
    # todo develop

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_s.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    # Wrap up
    # -------------------------------------------------------------------
    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


def compute_index_t(
    input_hand, input_twi, output_folder, hand_w=0.5, hand_max=15, twi_max=15
):
    # todo docstring

    # Startup
    # -------------------------------------------------------------------
    func_name = compute_index_t.__name__
    print(f"running: {func_name}")

    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = _make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_fuzzy_hand = f"{output_folder}/hand_f.tif"
    output_fuzzy_twi = f"{output_folder}/twi_f.tif"
    output_index_t = f"{output_folder}/index_t.tif"

    # Run processes
    # -------------------------------------------------------------------

    # fuzzify hand
    # -----------------------------------
    fuzzify(input_hand, output_fuzzy_hand, hand_max, 0)

    # fuzzify twi
    # -----------------------------------
    fuzzify(input_twi, output_fuzzy_twi, 0, twi_max)

    # get twi w
    # -----------------------------------
    twi_w = 1 - hand_w

    # get t formula
    # -----------------------------------
    s_expression = f'({hand_w} * "hand_f@1")  +  ({twi_w} *  "twi_f@1")'

    # run raster calculator
    # -----------------------------------
    processing.run(
        "native:rastercalc",
        {
            "LAYERS": [output_fuzzy_hand, output_fuzzy_twi],
            "EXPRESSION": s_expression,
            "EXTENT": None,
            "CELL_SIZE": None,
            "CRS": None,
            "OUTPUT": output_index_t,
        },
    )

    # Wrap up
    # -------------------------------------------------------------------

    print(f"run successfull. see for outputs:\n{output_folder}")

    return None


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
    output_folder = _make_run_folder(run_name=func_name, output_folder=output_folder)

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
    _save_gdf(gdf, db=output_file, layer=input_layer)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


# Demo example
# -----------------------------------------------------------------------
def process_data(input1, input2, output_folder):
    """
    Demo for processing data

    :param input1: file path to input data 1
    :type input1: str
    :param input2: file path to input data 1
    :type input2: str
    :param output_folder: file path to output folder
    :type output_folder: str
    """
    # Setup input variables
    # -------------------------------------------------------------------
    input1_basename = os.path.basename(input1)
    input1_name = input1_basename.split(".")[0]

    input2_basename = os.path.basename(input2)
    input2_name = input2_basename.split(".")[0]

    shutil.copy(src=input1, dst=f"{output_folder}/{input1_basename}")
    shutil.copy(src=input2, dst=f"{output_folder}/{input2_basename}")

    # Setup output variables
    # -------------------------------------------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------
    processing.run(
        "native:rastercalc",
        {
            "LAYERS": [input1, input2],
            "EXPRESSION": '"{}@1" * "{}@1"'.format(input1_name, input2_name),
            "EXTENT": None,
            "CELL_SIZE": None,
            "CRS": None,
            "OUTPUT": output_file,
        },
    )

    # Wrap up
    # -------------------------------------------------------------------

    return None


def fuzzify(input_file, output_file, low, hi):
    # Run processes
    # -------------------------------------------------------------------
    processing.run(
        "native:fuzzifyrasterlinearmembership",
        {
            "INPUT": input_file,
            "BAND": 1,
            "FUZZYLOWBOUND": low,
            "FUZZYHIGHBOUND": hi,
            "OUTPUT": output_file,
        },
    )
    return output_file


# ... {develop}


# FUNCTIONS -- Module-level
# =======================================================================
def waiter():
    print("hey!")
    time.sleep(3)


def get_timestamp():
    now = datetime.datetime.now()
    return str(now.strftime("%Y-%m-%dT%H%M%S"))


def _make_run_folder(run_name, folder_outputs):
    while True:
        ts = get_timestamp()
        folder_run = Path(folder_outputs) / f"{run_name}_{ts}"
        if os.path.exists(folder_run):
            time.sleep(1)
        else:
            os.mkdir(folder_run)
            break

    return os.path.abspath(folder_run)


def _save_gdf(gdf, db, layer):
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


# ... {develop}


# SCRIPT
# ***********************************************************************
# standalone behaviour as a script
if __name__ == "__main__":
    print("Hello World")
