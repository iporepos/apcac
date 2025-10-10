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
import time

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


def compute_t(input_hand, input_twi, output_folder, hand_max=15, hand_w=1, twi_max=30):

    # Setup input variables
    # -------------------------------------------------------------------

    # twi w
    # ----------------
    twi_w = 1 - hand_w

    # Setup output variables
    # -------------------------------------------------------------------
    os.makedirs(output_folder, exist_ok=True)
    # files
    # ----------------
    output_fuzzy_hand = f"{output_folder}/hand_f.tif"
    output_fuzzy_twi = f"{output_folder}/twi_f.tif"

    # Run processes
    # -------------------------------------------------------------------

    # fuzzify hand
    # ----------------
    fuzzify(input_hand, output_fuzzy_hand, hand_max, 0)

    # fuzzify twi
    # ----------------
    fuzzify(input_twi, output_fuzzy_twi, 0, twi_max)

    # Wrap up
    # -------------------------------------------------------------------

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


# ... {develop}


# SCRIPT
# ***********************************************************************
# standalone behaviour as a script
if __name__ == "__main__":
    print("Hello World")
