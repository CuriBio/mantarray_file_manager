# -*- coding: utf-8 -*-

import os
import tempfile

from freezegun import freeze_time
from mantarray_file_manager import BACKEND_LOG_UUID
from mantarray_file_manager import BARCODE_IS_FROM_SCANNER_UUID
from mantarray_file_manager import BasicWellFile
from mantarray_file_manager import COMPUTER_NAME_HASH_UUID
from mantarray_file_manager import CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import FILE_MIGRATION_PATHS
from mantarray_file_manager import FILE_VERSION_PRIOR_TO_MIGRATION_UUID
from mantarray_file_manager import file_writer
from mantarray_file_manager import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from mantarray_file_manager import MantarrayH5FileCreator
from mantarray_file_manager import migrate_to_latest_version
from mantarray_file_manager import migrate_to_next_version
from mantarray_file_manager import NOT_APPLICABLE_H5_METADATA
from mantarray_file_manager import ORIGINAL_FILE_VERSION_UUID
from mantarray_file_manager import TRIMMED_TIME_FROM_ORIGINAL_END_UUID
from mantarray_file_manager import TRIMMED_TIME_FROM_ORIGINAL_START_UUID
from mantarray_file_manager import UnsupportedFileMigrationPath
from mantarray_file_manager import UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID
from mantarray_file_manager import WELL_FILE_CLASSES
from mantarray_file_manager import WELL_INDEX_UUID
from mantarray_file_manager import WELL_NAME_UUID
from mantarray_file_manager import WellFile_0_3_1
from mantarray_file_manager import WellFile_0_4_1
import numpy as np
import pytest
from semver import VersionInfo
from stdlib_utils import get_current_file_abs_directory

from .fixtures import PATH_TO_GENERIC_0_3_1_FILE
from .fixtures import PATH_TO_GENERIC_0_4_1_FILE

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
        UnsupportedFileMigrationPath,
        match=f"0.1.*{CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION}",
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
        old_wf = WellFile_0_3_1(PATH_TO_GENERIC_0_3_1_FILE)
        assert wf.get_file_version() == "0.4.1"

        # old metadata (since it is all copied by default, testing a subset seems reasonable for now)
        assert wf.get_h5_attribute(str(WELL_INDEX_UUID)) == 9
        assert wf.get_h5_attribute(str(WELL_NAME_UUID)) == "B3"

        # new metadata
        assert not wf.get_h5_attribute(
            str(BARCODE_IS_FROM_SCANNER_UUID)
        )  # Eli (1/18/21): tried using `is False` but got weird errors saying `assert False is False` failed...unsure why
        assert wf.get_h5_attribute(str(IS_FILE_ORIGINAL_UNTRIMMED_UUID))
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 0
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 0
        assert wf.get_h5_attribute(str(BACKEND_LOG_UUID)) == str(NOT_APPLICABLE_H5_METADATA)
        assert wf.get_h5_attribute(str(COMPUTER_NAME_HASH_UUID)) == str(NOT_APPLICABLE_H5_METADATA)

        # raw data
        np.testing.assert_array_equal(wf.get_raw_tissue_reading(), old_wf.get_raw_tissue_reading())
        np.testing.assert_array_equal(
            wf.get_raw_reference_reading(), old_wf.get_raw_reference_reading()
        )

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
        old_wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


@freeze_time("2021-01-18 13:45:30.543221")
def test_migrate_to_next_version__When_invoked_on_a_0_4_1_file__Then_the_new_file_has_features_of_0_4_2__including_raw_data_old_metadata_and_new_metadata():
    old_version = "0.4.1"
    new_version = "0.4.2"

    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = migrate_to_next_version(
            PATH_TO_GENERIC_0_4_1_FILE, working_directory=tmp_dir
        )

        wf = WELL_FILE_CLASSES[new_version](new_file_path)
        old_wf = WELL_FILE_CLASSES[old_version](PATH_TO_GENERIC_0_4_1_FILE)
        assert wf.get_file_version() == new_version

        # old metadata (since it is all copied by default, testing a subset seems reasonable for now)
        assert (
            wf.get_h5_attribute(str(COMPUTER_NAME_HASH_UUID))
            == "8a1f943c08bf5de71ab50509532a6869962ce2b740d7491f8baf38a9caf12893df4507be47c69c74b90e9a1496d5952e891650561817e78e9388f2f63eb28065"
        )
        assert wf.get_h5_attribute(str(BACKEND_LOG_UUID)) == "a7f0199e-362a-41ca-9d4f-6c85f7df9cc7"

        # new metadata
        assert wf.get_h5_attribute(str(ORIGINAL_FILE_VERSION_UUID)) == str(
            NOT_APPLICABLE_H5_METADATA
        )
        assert wf.get_h5_attribute(str(FILE_VERSION_PRIOR_TO_MIGRATION_UUID)) == old_version
        assert (
            wf.get_h5_attribute(str(UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID))
            == "2021-01-18 13:45:30.543221"
        )

        # raw data
        np.testing.assert_array_equal(wf.get_raw_tissue_reading(), old_wf.get_raw_tissue_reading())
        np.testing.assert_array_equal(
            wf.get_raw_reference_reading(), old_wf.get_raw_reference_reading()
        )

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
        old_wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_migrate_to_latest_version__When_invoked_on_a_file_one_step_below_the_latest_version__Then_the_file_path_and_directory_are_passed_to_the_migrate_to_next_version_function(
    mocker,
):
    sorted_migration_versions = sorted([VersionInfo.parse(x) for x in FILE_MIGRATION_PATHS.keys()])
    latest_migration_path_version = str(sorted_migration_versions[-1])
    with tempfile.TemporaryDirectory() as tmp_dir:
        path_to_latest = os.path.join(tmp_dir, "latest.h5")
        latest_version_file = MantarrayH5FileCreator(path_to_latest)
        latest_version_file.close()
        path_to_next_to_latest = os.path.join(tmp_dir, "next-to-latest.h5")
        next_to_latest_version_file = MantarrayH5FileCreator(
            path_to_next_to_latest, file_format_version=latest_migration_path_version
        )
        next_to_latest_version_file.close()
        mocked_migrate_to_next_version = mocker.patch.object(
            file_writer,
            "migrate_to_next_version",
            autospec=True,
            return_value=path_to_latest,
        )
        migrate_to_latest_version(path_to_next_to_latest, working_directory=tmp_dir)

        mocked_migrate_to_next_version.assert_called_once_with(
            path_to_next_to_latest, working_directory=tmp_dir
        )


def test_migrate_to_latest_version__When_invoked_on_a_0_3_1_file__Then_the_returned_file_path_is_for_the_latest_version(
    mocker,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path_to_latest = migrate_to_latest_version(
            PATH_TO_GENERIC_0_3_1_FILE, working_directory=tmp_dir
        )

        assert path_to_latest.startswith(tmp_dir)
        latest_file = BasicWellFile(path_to_latest)
        assert latest_file.get_file_version() == CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
        latest_file.get_h5_file().close()
