# -*- coding: utf-8 -*-

import os
import tempfile

from mantarray_file_manager import CURRENT_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import MantarrayH5FileCreator
from mantarray_file_manager import migrate_to_latest_version
from mantarray_file_manager import UnsupportedFileMigrationPath
import pytest
from stdlib_utils import get_current_file_abs_directory

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()


def test_migrate_to_latest_version__When_invoked_on_a_file_that_is_already_the_latest_version__Then_it_returns_the_input_file_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        expected_filename = os.path.join(tmp_dir, "myfile.h5")
        test_file = MantarrayH5FileCreator(expected_filename)
        test_file.close()
        actual = migrate_to_latest_version(expected_filename)
    assert actual == expected_filename


def test_migrate_to_latest_version__When_invoked_on_a_file_with_no_migration_path_defined__Then_it_raises_an_error():
    path_to_0_1_file = os.path.join(
        PATH_OF_CURRENT_FILE, "h5", "v0.1", "MA20001100__2020_07_15_172203__A4.h5"
    )
    with pytest.raises(
        UnsupportedFileMigrationPath, match=f"0.1.*{CURRENT_HDF5_FILE_FORMAT_VERSION}"
    ):
        migrate_to_latest_version(path_to_0_1_file)
