# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2025 The Project Authors
# See pyproject.toml for authors/maintainers.
# See LICENSE for license details.
"""
Testing routines for the apcac.classes module

.. warning::

    Run this script in the QGIS python environment


"""

# IMPORTS
# ***********************************************************************
# import modules from other libs

# Native imports
# =======================================================================
import inspect
import shutil
from pathlib import Path
from pprint import pprint
import importlib.util as iu

# CONSTANTS
# ***********************************************************************
# ... {develop}

here = Path(__file__).resolve()
FOLDER_ROOT = here.parent.parent.parent
DATA_DIR = FOLDER_ROOT / "tests/data/V006"

# define the paths to this module
# ----------------------------------------
FILE_MODULE = FOLDER_ROOT / "src/apcac/classes.py"

# setup module with importlib
# ----------------------------------------
IU_SPEC = iu.spec_from_file_location("module", FILE_MODULE)
MODULE = iu.module_from_spec(IU_SPEC)
IU_SPEC.loader.exec_module(MODULE)

def test_analysis_apcac():
    # define the paths to input and output folders
    # ----------------------------------------
    output_dir = f"{DATA_DIR}/outputs"

    # define the path to input database
    # ----------------------------------------
    input_db = f"{DATA_DIR}/inputs/bho5k.gpkg"

    # define the paths to input rasters
    # ----------------------------------------
    raster_files = {
        # change this paths
        "t": f"{DATA_DIR}/inputs/indexes/chd_t_1000_01K_cerrado_o.tif",  # topography layer
        "s": f"{DATA_DIR}/inputs/indexes/chd_s_1000_01C_cerrado_o.tif",  # soil/pedology layer
        "g": f"{DATA_DIR}/inputs/indexes/chd_g_1000_001_cerrado_o.tif",  # geology/aquifers layer
        "c": f"{DATA_DIR}/inputs/indexes/chd_c_1000_01C_cerrado_1981u2010.tif",  # climate layer
        "n": f"{DATA_DIR}/inputs/indexes/chd_n_1000_001_cerrado_2018.tif",  # conservation layer
        "v": f"{DATA_DIR}/inputs/indexes/chd_v_1000_001_cerrado_2023.tif",  # anthropic risk layer
        "slope": f"{DATA_DIR}/inputs/variables/chd_sloped_0500_01C_cerrado_o.tif",  # terrain slope layer
        "uslek": f"{DATA_DIR}/inputs/variables/chd_uslek_0500_10K_cerrado_o.tif",  # erodibility layer
    }

    # define which index has multipliers (the value is divided)
    # ----------------------------------------
    raster_multipliers = {
        "t": 1000,
        "s": 100,
        "slope": 100,
        "c": 100
        # change and add more if needed
    }

    # call the function
    # ----------------------------------------
    MODULE.analysis_apcac(
        input_db=input_db,
        input_layer="apcac_bho5k",
        raster_files=raster_files,
        output_folder=output_dir,
        raster_multipliers=raster_multipliers,
        cleanup=True,
        skip_sampling=False,
    )


    # todo Assertions
    # ----------------------------------------

    return None

def main():
    print("hello")

    test_analysis_apcac()

    return None


main()

