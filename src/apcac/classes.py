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
]

FIELDS_INDEXES_INPUTS = ["t", "s", "g", "c", "n", "v", "slope", "uslek"]

N2 = 60
N1 = 10
V1 = -2
SLOPE_THRESHOLD = 5
USLEK_THRESHOLD = 300

# define constants in uppercase


# FUNCTIONS
# ***********************************************************************

# FUNCTIONS -- Project-level
# =======================================================================


def sample_indexes(
    input_db, raster_files, output_folder, layer="apcac_bho5k", raster_multipliers=None
):
    # todo docstring

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = rf"{output_folder}\apcac.gpkg"

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
                "INPUT": "{}|layername={}".format(input_db, layer),
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
    gdf = gpd.read_file(input_db, layer=layer)
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
    save_gdf(gdf, db=output_file, layer=layer)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def fuzzify_indexes(input_db, output_folder, layer="apcac_bho5k"):
    # todo docstring

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/apcac.gpkg"

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=layer)

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
    save_gdf(gdf, db=output_file, layer=layer)

    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_index_a(input_db, output_folder, layer="apcac_bho5k"):
    # todo docstring

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/apcac.gpkg"

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=layer)

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
    save_gdf(gdf, db=output_file, layer=layer)
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def compute_index_e(
    input_db,
    output_folder,
    layer="apcac_bho5k",
    n_threshold=None,
    slope_threshold=None,
    uslek_threshold=None,
):
    # todo docstring

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

    # files
    # -----------------------------------
    output_file = f"{output_folder}/apcac.gpkg"

    # variables
    # -----------------------------------

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=layer)

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
    save_gdf(gdf, db=output_file, layer=layer)
    print(f"run successfull. see for outputs:\n{output_folder}")

    return output_file


def upscale_apcac(input_db, output_folder):
    # todo docstring
    # todo develop
    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(
        run_name=compute_index_a.__name__, folder_outputs=output_folder
    )

    # files
    # -----------------------------------
    output_file = f"{output_folder}/result.tif"

    # Run processes
    # -------------------------------------------------------------------

    df["weighted_value"] = df["value"] * df["weight"]
    weighted_avg = (
        df.groupby("group")[["weighted_value", "weight"]]
        .sum()
        .eval("weighted_mean = weighted_value / weight")
        .reset_index()[["group", "weighted_mean"]]
    )

    # Wrap up
    # -------------------------------------------------------------------

    return None


def compute_apcac(input_db, output_folder, layer="apcac_bho5k"):
    # todo docstring
    # Setup input variables
    # -------------------------------------------------------------------

    # Setup output variables
    # -------------------------------------------------------------------

    # folders
    # -----------------------------------
    os.makedirs(output_folder, exist_ok=True)
    output_folder = make_run_folder(
        run_name=compute_apcac.__name__, folder_outputs=output_folder
    )

    # files
    # -----------------------------------
    output_file = f"{output_folder}/apcac.gpkg"

    # Run processes
    # -------------------------------------------------------------------

    # load data
    # -----------------------------------
    gdf = gpd.read_file(input_db, layer=layer)

    # compute apcac
    # -----------------------------------
    gdf = classify_apcac(gdf)

    # Export
    # -------------------------------------------------------------------

    # save
    # -----------------------------------
    save_gdf(gdf, db=output_file, layer=layer)
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


# ... {develop}


# FUNCTIONS -- Module-level
# =======================================================================
def waiter():
    print("hey!")
    time.sleep(3)


def get_timestamp():
    now = datetime.datetime.now()
    return str(now.strftime("%Y-%m-%dT%H%M%S"))


def make_run_folder(run_name, folder_outputs):
    while True:
        ts = get_timestamp()
        folder_run = Path(folder_outputs) / f"{run_name}_{ts}"
        if os.path.exists(folder_run):
            time.sleep(1)
        else:
            os.mkdir(folder_run)
            break

    return os.path.abspath(folder_run)


def fuzzify(v, v_lo, v_up):
    # apply function
    v_f = fuzzify_linear(v, v_lo, v_up)
    # get bounds
    v_lo_bool = np.where(v < v_lo, 0, 1)
    v_up_bool = np.where(v > v_up, 0, 1)
    # return boolean product
    return v_f * v_lo_bool * v_up_bool


def fuzzify_linear(v, v_lo=None, v_up=None):
    """
    Fuzzify a NumPy array to [0, 1] ignoring NaNs, preserving them in the result.
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


def save_gdf(gdf, db, layer):
    # organize columns
    my_list = list(gdf.columns)
    item = my_list.pop(my_list.index("geometry"))  # remove and get the item
    my_list.append(item)
    gdf = gdf[my_list].copy()

    print(" >> saving...")
    gdf.to_file(db, layer=layer, driver="GPKG")
    return None


def classify_apcac(gdf):
    # todo docstring
    # CLASSIFY
    # level 2 -- natural or anthropic
    gdf["cd_apcac_n"] = np.where(gdf["n"] >= N2, "I", "II")
    gdf["id_apcac_n"] = np.where(gdf["n"] >= N2, 100, 200)
    gdf["id_apcac_n"] = gdf["id_apcac_n"].astype(int)

    # level 2 --- hydrology
    gdf["a"] = gdf["a"].fillna(0)
    thresholds = [
        0,
        np.percentile(gdf["a"].values, 40),
        np.percentile(gdf["a"].values, 70),
        np.percentile(gdf["a"].values, 90),
        np.inf,
    ]
    print(thresholds)
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
    # risk in natural catchments
    gdf_n["cd_apcac_risk"] = np.where(gdf_n["v"] <= V1, "R", "N")
    gdf_n["id_apcac_risk"] = np.where(gdf_n["v"] <= V1, 2, 1)
    gdf_n["id_apcac_risk"] = gdf_n["id_apcac_risk"].astype(int)

    # risk in anthropic catchments
    gdf_a["cd_apcac_risk"] = np.where(gdf_a["e"] > 0, "R", "N")
    gdf_a["id_apcac_risk"] = np.where(gdf_a["e"] > 0, 2, 1)

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


# ... {develop}


# SCRIPT
# ***********************************************************************
# standalone behaviour as a script
if __name__ == "__main__":

    print("Hello World")
