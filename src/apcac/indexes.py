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
import processing


# ... {develop}

# Project-level imports
# =======================================================================
# import {module}
# ... {develop}


# CONSTANTS
# ***********************************************************************
# define constants in uppercase


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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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
    output_folder = make_run_folder(run_name=func_name, folder_outputs=output_folder)

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


# ... {develop}


# SCRIPT
# ***********************************************************************
# standalone behaviour as a script
if __name__ == "__main__":
    print("Hello World")
