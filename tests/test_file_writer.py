# -*- coding: utf-8 -*-

import os
import tempfile

from immutable_data_validation.errors import ValidationCollectionMinimumValueError
from immutable_data_validation.errors import ValidationCollectionNotAnIntegerError
from mantarray_file_manager import BasicWellFile
from mantarray_file_manager import CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import file_writer
from mantarray_file_manager import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from mantarray_file_manager import MantarrayFileNotLatestVersionError
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

from .fixtures import fixture_current_beta1_version_file_path
from .fixtures import fixture_current_beta2_version_file_path
from .fixtures import fixture_trimmed_file_path

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()

__fixtures__ = (
    fixture_current_beta1_version_file_path,
    fixture_trimmed_file_path,
    fixture_current_beta2_version_file_path,
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
        assert test_file.attrs["File Format Version"] == CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION

        wf.get_h5_file().close()  # cleanup when running CI on windows systems


def test_h5_file_trimmer__uses_cwd_when_a_file_dir_is_not_specified(
    current_beta1_version_file_path, mocker
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        mocker.patch.object(file_writer, "getcwd", autospec=True, return_value=tmp_dir)
        new_file_path = h5_file_trimmer(current_beta1_version_file_path, from_start=1)
        assert tmp_dir in new_file_path


def test_h5_file_trimmer__When_start_arg_is_negative__Then_raises_an_error(
    current_beta1_version_file_path,
):
    with pytest.raises(ValidationCollectionMinimumValueError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=-10, from_end=0)


def test_h5_file_trimmer__When_start_arg_is_not_an_int__Then_raises_an_error(
    current_beta1_version_file_path,
):
    with pytest.raises(ValidationCollectionNotAnIntegerError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=1.7, from_end=0)


def test_h5_file_trimmer__When_start_args_are_both_0__Then_raises_an_error(
    current_beta1_version_file_path,
):
    with pytest.raises(UnsupportedArgumentError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=0, from_end=0)


def test_h5_file_trimmer__When_end_arg_is_not_valid__Then_raises_an_error(
    current_beta1_version_file_path,
):
    with pytest.raises(ValidationCollectionMinimumValueError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=0, from_end=-1)


def test_h5_file_trimmer__When_both_args_are_None__Then_raises_an_error(
    current_beta1_version_file_path,
):
    with pytest.raises(UnsupportedArgumentError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=None, from_end=None)


def test_h5_file_trimmer__When_file_path_isnt_supported__Then_raises_an_error():
    EXPECTED_PATH_D6 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D6.h5",
    )
    with pytest.raises(MantarrayFileNotLatestVersionError) as excinfo:
        h5_file_trimmer(EXPECTED_PATH_D6, from_start=10, from_end=10)
    assert CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION in str(excinfo.value)


def test_h5_file_trimmer__When_invoked_on_a_file__Then_the_new_file_has_old_metadata_except_for_the_three_metadata_pertaining_to_trimming(
    current_beta1_version_file_path,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(current_beta1_version_file_path, tmp_dir, 200, 200)

        wf = WellFile(new_file_path)
        old_wf = WellFile(current_beta1_version_file_path)

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
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 160
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 160

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
        old_wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_file_with_too_much_time_trimmed__Then_raises_TooTrimmedError(
    current_beta1_version_file_path,
):
    with pytest.raises(TooTrimmedError):
        h5_file_trimmer(current_beta1_version_file_path, from_start=6000000, from_end=2000000)


def test_h5_file_trimmer__When_invoked_on_a_current_file_with_args_in_before_time_points__Then_the_new_file_has_trimmed_raw_referene_and_tissue_data(
    current_beta1_version_file_path,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(current_beta1_version_file_path, tmp_dir, 70, 70)

        wf = WellFile(new_file_path)

        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 0
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 0

        # raw data
        tissue_data = wf.get_raw_tissue_reading()
        assert tissue_data[0][0] == 120
        assert tissue_data[0][-1] == 135960
        assert tissue_data[1][0] == -974940
        assert tissue_data[1][-1] == 1737936

        reference_data = wf.get_raw_reference_reading()
        assert reference_data[0][0] == 20
        assert reference_data[0][-1] == 1182980
        assert reference_data[1][0] == -2722104
        assert reference_data[1][-1] == -4190110

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_current_file_with_args_on_time_points__Then_the_new_file_has_trimmed_raw_referene_and_tissue_data(
    current_beta1_version_file_path,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(current_beta1_version_file_path, tmp_dir, 320, 320)

        wf = WellFile(new_file_path)

        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 320
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 320

        # raw data
        tissue_data = wf.get_raw_tissue_reading()
        assert tissue_data[0][0] == 440
        assert tissue_data[0][-1] == 135640
        assert tissue_data[1][0] == -950718
        assert tissue_data[1][-1] == 1713713

        reference_data = wf.get_raw_reference_reading()
        assert reference_data[0][0] == 340
        assert reference_data[0][-1] == 1182660
        assert reference_data[1][0] == -2654995
        assert reference_data[1][-1] == -4123001

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_current_file_with_only_end_arg__Then_the_new_file_has_trimmed_raw_referene_and_tissue_data(
    current_beta1_version_file_path,
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(current_beta1_version_file_path, tmp_dir, from_end=320)

        wf = WellFile(new_file_path)

        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 0
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 320

        # raw data
        tissue_data = wf.get_raw_tissue_reading()
        assert tissue_data[0][0] == 120
        assert tissue_data[0][-1] == 135640
        assert tissue_data[1][0] == -974940
        assert tissue_data[1][-1] == 1713713

        reference_data = wf.get_raw_reference_reading()
        assert reference_data[0][0] == 20
        assert reference_data[0][-1] == 1182660
        assert reference_data[1][0] == -2722104
        assert reference_data[1][-1] == -4123001

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__When_invoked_on_a_trimmed_file__Then_the_new_file_is_additionally_trimmed_with_the_raw_reference_tissue_data_and_metadata_updated(
    trimmed_file_path,
    mocker,
):
    mocked_print = mocker.patch.object(file_writer, "_print", autospec=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(trimmed_file_path, tmp_dir, 200, 200)

        mocked_trimmed_str = "160 centimilliseconds"
        assert mocked_trimmed_str in mocked_print.call_args_list[0][0][0]
        assert mocked_trimmed_str in mocked_print.call_args_list[1][0][0]

        wf = WellFile(new_file_path)

        assert not wf.get_h5_attribute(
            str(IS_FILE_ORIGINAL_UNTRIMMED_UUID)
        )  # Anna (1/20/21): tried using `is False` but got weird errors saying `assert False is False` failed...unsure why
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 480
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 480

        # raw data
        tissue_data = wf.get_raw_tissue_reading()
        assert tissue_data[0][0] == 600
        assert tissue_data[0][-1] == 135480
        assert tissue_data[1][0] == -938607
        assert tissue_data[1][-1] == 1701602

        reference_data = wf.get_raw_reference_reading()
        assert reference_data[0][0] == 500
        assert reference_data[0][-1] == 1182500
        assert reference_data[1][0] == -2621441
        assert reference_data[1][-1] == -4089447

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems


def test_h5_file_trimmer__correctly_trims_beta_2_file(current_beta2_version_file_path):
    with tempfile.TemporaryDirectory() as tmp_dir:
        new_file_path = h5_file_trimmer(current_beta2_version_file_path, tmp_dir, 1000, 1000)
        wf = WellFile(new_file_path)

        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)) == 1000
        assert wf.get_h5_attribute(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)) == 1000

        tissue_data = wf.get_raw_tissue_reading()
        assert tissue_data[0][0] == -6120
        assert tissue_data[0][-1] == 880
        assert tissue_data[1][0] == 1
        assert tissue_data[1][-1] == 8
        assert tissue_data[9][0] == 81
        assert tissue_data[9][-1] == 88

        tissue_data = wf.get_raw_reference_reading()
        assert tissue_data[0][0] == -6960
        assert tissue_data[0][-1] == 40
        assert tissue_data[1][0] == 1
        assert tissue_data[1][-1] == 8
        assert tissue_data[9][0] == 81
        assert tissue_data[9][-1] == 88

        wf.get_h5_file().close()  # safe clean-up when running CI on windows systems
