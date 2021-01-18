# -*- coding: utf-8 -*-

import os
import tempfile

from mantarray_file_manager import BARCODE_IS_FROM_SCANNER_UUID
from mantarray_file_manager import CURRENT_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import file_writer
from mantarray_file_manager import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from mantarray_file_manager import MantarrayH5FileCreator
from mantarray_file_manager import migrate_to_next_version
from mantarray_file_manager import UnsupportedFileMigrationPath
from mantarray_file_manager import WELL_INDEX_UUID
from mantarray_file_manager import WELL_NAME_UUID
from mantarray_file_manager import WellFile_0_4_1
import pytest
from stdlib_utils import get_current_file_abs_directory

from .fixtures import PATH_TO_GENERIC_0_3_1_FILE

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()


def test_migrate_to_next_version__When_invoked_on_a_file_that_is_already_the_latest_version__Then_it_returns_the_input_file_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        expected_filename = os.path.join(tmp_dir, "myfile.h5")
        test_file = MantarrayH5FileCreator(expected_filename)
        test_file.close()
        actual = migrate_to_next_version(expected_filename)
    assert actual == expected_filename


def test_migrate_to_next_version__When_invoked_on_a_file_with_no_migration_path_defined__Then_it_raises_an_error():
    path_to_0_1_file = os.path.join(
        PATH_OF_CURRENT_FILE, "h5", "v0.1", "MA20001100__2020_07_15_172203__A4.h5"
    )
    with pytest.raises(
        UnsupportedFileMigrationPath, match=f"0.1.*{CURRENT_HDF5_FILE_FORMAT_VERSION}"
    ):
        migrate_to_next_version(path_to_0_1_file)


def test_migrate_to_next_version__When_invoked_on_a_0_3_1_file_with_no_working_directory_kwarg__Then_the_new_file_is_created_in_the_current_working_directory(
    mocker,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        mocker.patch.object(file_writer, "getcwd", autospec=True, return_value=tmp_dir)
        new_file_path = migrate_to_next_version(PATH_TO_GENERIC_0_3_1_FILE)
        assert new_file_path.startswith(tmp_dir)


def test_migrate_to_next_version__When_invoked_on_a_0_3_1_file__Then_the_new_file_has_features_of_0_4_1__including_raw_data_old_metadata_and_new_metadata():
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = migrate_to_next_version(
            PATH_TO_GENERIC_0_3_1_FILE, working_directory=tmp_dir
        )
        wf = WellFile_0_4_1(new_file_path)
        assert wf.get_file_version() == "0.4.1"

        # old metadata (since it is all copied by default, testing a subset seems reasonable for now)
        assert wf.get_h5_attribute(str(WELL_INDEX_UUID)) == 9
        assert wf.get_h5_attribute(str(WELL_NAME_UUID)) == "B3"

        # new metadata
        assert not wf.get_h5_attribute(
            str(BARCODE_IS_FROM_SCANNER_UUID)
        )  # Eli (1/18/21): tried using `is False` but got weird errors saying `assert False is False` failed...unsure why
        assert wf.get_h5_attribute(str(IS_FILE_ORIGINAL_UNTRIMMED_UUID))
