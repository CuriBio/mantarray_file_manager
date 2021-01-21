# -*- coding: utf-8 -*-

import os
import tempfile

from immutable_data_validation.errors import ValidationCollectionMinimumValueError
from immutable_data_validation.errors import ValidationCollectionNotAnIntegerError
from mantarray_file_manager import BasicWellFile
from mantarray_file_manager import CURRENT_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from mantarray_file_manager import MantarrayH5FileCreator
from mantarray_file_manager import TRIMMED_TIME_FROM_ORIGINAL_END_UUID
from mantarray_file_manager import TRIMMED_TIME_FROM_ORIGINAL_START_UUID
from mantarray_file_manager import WELL_INDEX_UUID
from mantarray_file_manager import WELL_NAME_UUID
from mantarray_file_manager import WellFile
from mantarray_file_manager.exceptions import TooTrimmedError
from mantarray_file_manager.exceptions import UnsupportedArgumentError
from mantarray_file_manager.file_writer import h5_file_trimmer
import pytest
from stdlib_utils import get_current_file_abs_directory

from .fixtures import PATH_TO_GENERIC_0_4_1_FILE

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()

EXPECTED_PATH = os.path.join(
    PATH_OF_CURRENT_FILE,
    "2020_08_04_build_775",
    "MA20001010__2020_08_04_220041__D6.h5",
)


def test_MantarrayH5FileCreator__sets_file_name_and_userblock_size_and_file_version():
    with tempfile.TemporaryDirectory() as tmp_dir:
        expected_filename = os.path.join(tmp_dir, "myfile.h5")
        test_file = MantarrayH5FileCreator(expected_filename)
        test_file.close()
        wf = BasicWellFile(expected_filename)
        test_file = wf.get_h5_file()
        assert test_file.userblock_size == 512
        assert test_file.filename == expected_filename
        assert (
            test_file.attrs["File Format Version"] == CURRENT_HDF5_FILE_FORMAT_VERSION
        )

        wf.get_h5_file().close()  # cleanup when running CI on windows systems


def test_h5_file_trimmer__When_start_arg_is_negative__Then_raises_an_error():
    with pytest.raises(ValidationCollectionMinimumValueError):
        h5_file_trimmer(EXPECTED_PATH, from_start=-10, from_end=0)


def test_h5_file_trimmer__When_start_arg_is_not_an_int__Then_raises_an_error():
    with pytest.raises(ValidationCollectionNotAnIntegerError):
        h5_file_trimmer(EXPECTED_PATH, from_start=1.7, from_end=0)


def test_h5_file_trimmer__When_end_arg_is_not_valid__Then_raises_an_error():
    with pytest.raises(ValidationCollectionMinimumValueError):
        h5_file_trimmer(EXPECTED_PATH, from_start=0, from_end=-1)


def test_h5_file_trimmer__When_both_args_are_None__Then_raises_an_error():
    with pytest.raises(UnsupportedArgumentError):
        h5_file_trimmer(EXPECTED_PATH, from_start=None, from_end=None)


def test_h5_file_trimmer__When_invoked_on_a_file__Then_the_new_file_has_old_metadata_except_for_the_three_metadata_pertaining_to_trimming():
    new_file_path = h5_file_trimmer(PATH_TO_GENERIC_0_4_1_FILE, 0, 1)

    wf = WellFile(new_file_path)
    old_wf = WellFile(PATH_TO_GENERIC_0_4_1_FILE)

    # old metadata (since it is all copied by default, testing a subset seems reasonable for now)
    assert wf.get_h5_attribute(str(WELL_INDEX_UUID)) == old_wf.get_h5_attribute(
        str(WELL_INDEX_UUID)
    )
    assert wf.get_h5_attribute(str(WELL_NAME_UUID)) == old_wf.get_h5_attribute(
        str(WELL_NAME_UUID)
    )

    # new metadata
    assert not wf.get_h5_attribute(
        str(IS_FILE_ORIGINAL_UNTRIMMED_UUID)
    )  # Anna (1/20/21): tried using `is False` but got weird errors saying `assert False is False` failed...unsure why
    assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 0
    assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 1

    wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
    old_wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_file_with_too_much_time_trimmed__Then_raises_TooTrimmedError():
    with pytest.raises(TooTrimmedError):
        h5_file_trimmer(EXPECTED_PATH, from_start=6000000, from_end=2000000)


def test_h5_file_trimmer__When_invoked_on_a_0_4_1_file_with_args_in_between_time_points__Then_the_new_file_has_trimmed_raw_referene_and_tissue_data():
    new_file_path = h5_file_trimmer(PATH_TO_GENERIC_0_4_1_FILE, 70, 70)

    wf = WellFile(new_file_path)

    # raw data
    reference_data = wf.get_raw_reference_reading()
    # assert raw_reference_data[0][0] == 60
    assert reference_data[1][0] == -2713715
    # assert raw_reference_data[0][-1] == 1182940
    assert reference_data[1][-1] == -4181722

    tissue_data = wf.get_raw_tissue_reading()
    assert tissue_data[1][0] == -974940
    assert tissue_data[1][-1] == 1737936

    wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_0_4_1_file_with_args_on_time_points__Then_the_new_file_has_trimmed_raw_referene_and_tissue_data():
    new_file_path = h5_file_trimmer(PATH_TO_GENERIC_0_4_1_FILE, 100, 80)

    wf = WellFile(new_file_path)

    # raw data
    reference_data = wf.get_raw_reference_reading()
    # assert raw_reference_data[0][0] == 60
    assert reference_data[1][0] == -2705327
    # assert raw_reference_data[0][-1] == 1182940
    assert reference_data[1][-1] == -4173333

    tissue_data = wf.get_raw_tissue_reading()
    assert tissue_data[1][0] == -974940
    assert tissue_data[1][-1] == 1737936

    wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
