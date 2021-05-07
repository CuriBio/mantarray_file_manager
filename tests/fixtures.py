# -*- coding: utf-8 -*-
import os
import tempfile

from mantarray_file_manager import migrate_to_latest_version
from mantarray_file_manager import WellFile
from mantarray_file_manager.file_writer import h5_file_trimmer
import pytest
from stdlib_utils import get_current_file_abs_directory

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()

PATH_TO_GENERIC_0_3_1_FILE = os.path.join(
    PATH_OF_CURRENT_FILE,
    "h5",
    "v0.3.1",
    "MA20123456__2020_08_17_145752__B3.h5",
)

PATH_TO_GENERIC_0_4_1_FILE = os.path.join(
    PATH_OF_CURRENT_FILE,
    "h5",
    "v0.4.1",
    "MA190190000__2021_01_19_011931__C3.h5",
)


@pytest.fixture(scope="module", name="current_beta1_version_file_path")
def fixture_current_beta1_version_file_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(
            PATH_OF_CURRENT_FILE,
            "h5",
            "v0.4.2",
            "MA190190000__2021_01_19_011931__C3__v0.4.2.h5",
        )
        new_file_path = migrate_to_latest_version(file_path, tmp_dir)
        yield new_file_path


@pytest.fixture(scope="module", name="trimmed_file_path")
def fixture_trimmed_file_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(
            PATH_OF_CURRENT_FILE,
            "h5",
            "v0.4.2",
            "MA190190000__2021_01_19_011931__C3__v0.4.2.h5",
        )
        new_file_path = migrate_to_latest_version(file_path, tmp_dir)
        trimmed_file_path = h5_file_trimmer(new_file_path, tmp_dir, 320, 320)
        yield trimmed_file_path


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


@pytest.fixture(scope="function", name="generic_well_file_0_3_1")
def fixture_generic_well_file_0_3_1():
    wf = WellFile(PATH_TO_GENERIC_0_3_1_FILE)
    yield wf


@pytest.fixture(scope="function", name="generic_well_file_0_3_1__2")
def fixture_generic_well_file_0_3_1__2():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "h5",
            "v0.3.1",
            "MA20123456__2020_08_17_145752__A2.h5",
        )
    )
    yield wf


@pytest.fixture(scope="module", name="current_beta2_version_file_path")
def fixture_current_beta2_version_file_path():
    # TODO Tanner (5/6/21): replace this with a real beta 2 file as soon as one is made and update the tests that use this file
    yield os.path.join(PATH_OF_CURRENT_FILE, "beta_2_h5", "v1.0.0", "dummy.h5")


@pytest.fixture(scope="function", name="generic_well_file_1_0_0")
def fixture_generic_well_file_1_0_0():
    # TODO see note in fixture above
    wf = WellFile(os.path.join(PATH_OF_CURRENT_FILE, "beta_2_h5", "v1.0.0", "dummy.h5"))
    yield wf
