# -*- coding: utf-8 -*-

import os
import tempfile

from immutable_data_validation.errors import ValidationCollectionMinimumValueError
from immutable_data_validation.errors import ValidationCollectionNotAnIntegerError
from mantarray_file_manager import BasicWellFile
from mantarray_file_manager import CURRENT_HDF5_FILE_FORMAT_VERSION
from mantarray_file_manager import MantarrayH5FileCreator
from mantarray_file_manager.file_writer import h5_file_trimmer
import pytest
from stdlib_utils import get_current_file_abs_directory

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
