# -*- coding: utf-8 -*-
import os

from mantarray_file_manager import WellFile
import pytest
from stdlib_utils import get_current_file_abs_directory

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()


@pytest.fixture(scope="function", name="generic_well_file")
def fixture_generic_well_file():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__A3.h5",
        )
    )
    yield wf