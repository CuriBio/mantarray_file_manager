# -*- coding: utf-8 -*-

import datetime
import os
import time
from uuid import UUID

import h5py
from immutabledict import immutabledict
from mantarray_file_manager import BasicWellFile
from mantarray_file_manager import FILE_FORMAT_VERSION_METADATA_KEY
from mantarray_file_manager import FileAttributeNotFoundError
from mantarray_file_manager import files
from mantarray_file_manager import METADATA_UUID_DESCRIPTIONS
from mantarray_file_manager import MIN_SUPPORTED_FILE_VERSION
from mantarray_file_manager import PlateRecording
from mantarray_file_manager import UnsupportedMantarrayFileVersionError
from mantarray_file_manager import USER_ACCOUNT_ID_UUID
from mantarray_file_manager import WELL_FILE_CLASSES
from mantarray_file_manager import WellFile
from mantarray_file_manager import WellFile_0_3_1
from mantarray_file_manager import WellFile_0_4_1
from mantarray_file_manager import WellFile_0_4_2
from mantarray_file_manager import WellRecordingsNotFromSameSessionError
import numpy as np
import pytest
from stdlib_utils import get_current_file_abs_directory

from .fixtures import fixture_generic_well_file
from .fixtures import fixture_generic_well_file_0_3_1
from .fixtures import fixture_generic_well_file_0_3_1__2
from .fixtures import fixture_generic_well_file_1_0_0
from .fixtures import fixture_trimmed_file_path

__fixtures__ = (
    fixture_generic_well_file,
    fixture_generic_well_file_0_3_1,
    fixture_generic_well_file_0_3_1__2,
    fixture_trimmed_file_path,
    fixture_generic_well_file_1_0_0,
)
PATH_OF_CURRENT_FILE = get_current_file_abs_directory()


def test_BasicWellFile__opens_file_and_gets_file_version():
    expected_path = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D6.h5",
    )
    bwf = BasicWellFile(expected_path)
    assert bwf.get_file_version() == "0.2.1"
    assert isinstance(bwf.get_h5_file(), h5py.File)
    assert bwf.get_file_name() == expected_path


def test_BasicWellFile__When_deleted__Then_it_closes_the_h5_file(mocker):
    bwf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__D6.h5",
        )
    )
    spied_close = mocker.spy(bwf.get_h5_file(), "close")
    del bwf
    spied_close.assert_called_once()


def test_WellFile__opens_and_get_file_version():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__D6.h5",
        )
    )
    assert wf.get_file_version() == "0.2.1"


def test_WellFile__opens_and_get_well_name():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__D6.h5",
        )
    )
    assert wf.get_well_name() == "D6"


def test_WellFile__opens_and_get_well_index():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__D6.h5",
        )
    )
    assert wf.get_well_index() == 23


def test_WellFile__opens_and_get_plate_barcode():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )
    assert wf.get_plate_barcode() == "M120171010"


def test_WellFile__opens_and_get_user_account():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__D6.h5",
        )
    )
    assert wf.get_user_account() == UUID("455b93eb-c78f-4494-9f73-d3291130f126")


def test_WellFile__get_unique_recording_key(generic_well_file):
    assert generic_well_file.get_unique_recording_key() == (
        "MA20001010",
        datetime.datetime(2020, 8, 4, 22, 1, 27, 491628, tzinfo=datetime.timezone.utc),
    )


def test_WellFile__opens_and_get_customer_account():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )
    assert wf.get_customer_account() == UUID("73f52be0-368c-42d8-a1fd-660d49ba5604")


def test_WellFile__returns_time_index_of_request_to_start_recording(
    generic_well_file_0_3_1,
):
    actual = generic_well_file_0_3_1.get_recording_start_index()
    assert actual == 392000


def test_WellFile__get_timestamp_of_beginning_of_data_acquisition(
    generic_well_file_0_3_1,
):
    actual = generic_well_file_0_3_1.get_timestamp_of_beginning_of_data_acquisition()
    assert actual == datetime.datetime(
        2020, 8, 17, 14, 57, 48, 189863, tzinfo=datetime.timezone.utc
    )


def test_WellFile__opens_and_get_mantarray_serial_number():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )
    assert wf.get_mantarray_serial_number() == "M02001900"


def test_WellFile__opens_and_get_begin_recording():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "2020_08_04_build_775",
            "MA20001010__2020_08_04_220041__A1.h5",
        )
    )

    assert wf.get_begin_recording() == datetime.datetime(
        2020, 8, 4, 22, 1, 27, 491628, tzinfo=datetime.timezone.utc
    )


def test_WellFile__get_raw_tissue_reading__has_correct_time_offset_at_index_0(
    generic_well_file_0_3_1,
):
    arr = generic_well_file_0_3_1.get_raw_tissue_reading()
    assert arr.shape == (2, 370)
    assert arr.dtype == np.int32
    assert arr[0, 0] == 880
    assert arr[1, 0] == -1230373

    expected_timestep = 960  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep
    assert arr[1, 150] == 817496


def test_WellFile__get_raw_tissue_reading__has_correct_time_offset_at_index_0_when_trimmed(
    trimmed_file_path,
):
    wf = WellFile(trimmed_file_path)
    arr = wf.get_raw_tissue_reading()
    assert arr.shape == (2, 846)
    assert arr.dtype == np.int32
    assert arr[0, 0] == 440
    assert arr[1, 0] == -950718

    expected_timestep = 160  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep


def test_WellFile__get_raw_reference_reading__has_correct_time_offset_at_index_0(
    generic_well_file_0_3_1,
):
    arr = generic_well_file_0_3_1.get_raw_reference_reading()
    assert arr.shape == (
        2,
        6706,  # Tanner (9/29/20): The reason this number is not the same as the number of tissue readings from the same file is likely due to an issue with with Mantarray Desktop App recording duplicate reference data
    )
    assert arr.dtype == np.int32
    assert arr[0, 0] == 40
    assert arr[1, 0] == -1429419

    expected_timestep = (
        960 // 4
    )  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep
    assert arr[1, 150] == 255013


def test_WellFile__get_raw_reference_reading__has_correct_time_offset_at_index_0_when_trimmed(
    trimmed_file_path,
):
    wf = WellFile(trimmed_file_path)
    arr = wf.get_raw_reference_reading()
    assert arr.shape == (2, 29559)
    assert arr.dtype == np.int32
    assert arr[0, 0] == 340
    assert arr[1, 0] == -2654995

    expected_timestep = 40  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep


def test_WellFile_beta_2__get_raw_tissue_reading__has_correct_time_offset_at_index_0(
    generic_well_file_1_0_0,
):
    arr = generic_well_file_1_0_0.get_raw_tissue_reading()
    assert arr.shape == (10, 10)
    assert arr.dtype == np.int32
    assert arr[1, 0] == 0
    assert arr[9, 9] == 89

    expected_timestep = 1000  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep


def test_WellFile_beta_2__get_raw_reference_reading__has_correct_time_offset_at_index_0(
    generic_well_file_1_0_0,
):
    arr = generic_well_file_1_0_0.get_raw_reference_reading()
    assert arr.shape == (10, 10)
    assert arr.dtype == np.int32
    assert arr[1, 0] == 0
    assert arr[9, 9] == 89

    expected_timestep = 1000  # future versions of H5 files might not have a method to retrieve the sampling period (because that concept may cease to exist), so here it is hard coded to what the period is for v0.3.1
    assert arr[0, 1] - arr[0, 0] == expected_timestep


def test_WellFile__get_h5_attribute__can_access_arbitrary_metadata(
    generic_well_file_0_3_1,
):
    assert generic_well_file_0_3_1.get_h5_attribute(FILE_FORMAT_VERSION_METADATA_KEY) == "0.3.1"


def test_WellFile__get_h5_file__returns_file_object(generic_well_file_0_3_1):
    assert isinstance(generic_well_file_0_3_1.get_h5_file(), h5py.File) is True


def test_WellFile__get_h5_attribute__raises_error_if_attribute_is_not_found():
    file_ver = "0.3.1"
    file_path = os.path.join(
        PATH_OF_CURRENT_FILE,
        "h5",
        f"v{file_ver}",
        "MA20123456__2020_08_17_145752__A1.h5",
    )
    wf = WellFile(file_path)
    test_attr = "fake_attr"
    with pytest.raises(FileAttributeNotFoundError) as excinfo:
        wf.get_h5_attribute(test_attr)
    assert "no UUID given" in str(excinfo.value)
    assert file_ver in str(excinfo.value)
    assert file_path in str(excinfo.value)
    assert test_attr in str(excinfo.value)


def test_WellFile__get_h5_attribute__raises_error_with_UUID_and_description_if_UUID_attribute_is_not_found():
    file_ver = "0.1"
    file_path = os.path.join(
        PATH_OF_CURRENT_FILE,
        "h5",
        f"v{file_ver}",
        "MA20001100__2020_07_15_172203__A4.h5",
    )
    wf = WellFile(file_path)
    test_attr = USER_ACCOUNT_ID_UUID
    test_attr_description = METADATA_UUID_DESCRIPTIONS[USER_ACCOUNT_ID_UUID]
    with pytest.raises(FileAttributeNotFoundError) as excinfo:
        wf.get_h5_attribute(str(test_attr))
    assert str(test_attr) in str(excinfo.value)
    assert file_ver in str(excinfo.value)
    assert file_path in str(excinfo.value)
    assert test_attr_description in str(excinfo.value)
    assert "no UUID given" not in str(excinfo.value)


def test_WellFile__get_h5_attribute__raises_error_with_unrecognized_UUID__if_UUID_attribute_is_not_found():
    file_ver = "0.1"
    file_path = os.path.join(
        PATH_OF_CURRENT_FILE,
        "h5",
        f"v{file_ver}",
        "MA20001100__2020_07_15_172203__A4.h5",
    )
    wf = WellFile(file_path)
    test_uuid = UUID("e07bae2d-c927-490f-876b-a7a79c2369e7")
    with pytest.raises(FileAttributeNotFoundError) as excinfo:
        wf.get_h5_attribute(str(test_uuid))
    assert str(test_uuid) in str(excinfo.value)
    assert file_ver in str(excinfo.value)
    assert file_path in str(excinfo.value)
    assert "Unrecognized UUID" in str(excinfo.value)


def test_PlateRecording__from_directory__creates_a_plate_recording_with_all_h5_files_in_the_directory():
    pr = PlateRecording.from_directory(os.path.join(PATH_OF_CURRENT_FILE, "h5", "v0.3.1"))
    assert len(pr.get_well_names()) == 24


def test_PlateRecording__opens_and_get_wellfile_names():
    wf1 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D1.h5",
    )
    wf2 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D2.h5",
    )
    wf3 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D3.h5",
    )
    wf4 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D4.h5",
    )
    wf5 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D5.h5",
    )
    wf6 = os.path.join(
        PATH_OF_CURRENT_FILE,
        "2020_08_04_build_775",
        "MA20001010__2020_08_04_220041__D6.h5",
    )

    file_list = PlateRecording([wf1, wf2, wf3, wf4, wf5, wf6])

    assert np.size(file_list.get_wellfile_names()) == 6


def test_get_unique_files():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    assert len(unique_files) == 24


def test_get_files_by_well_name():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    dictionary = files.get_specified_files("Well Name", "D6", unique_files)

    assert len(dictionary["Well Name"]["D6"]) == 1


def test_get_files_by_plate_barcode():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    dictionary = files.get_specified_files("Plate Barcode", "MA20001010", unique_files)

    assert len(dictionary["Plate Barcode"]["MA20001010"]) == 24


def test_get_files_by_user():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    dictionary = files.get_specified_files(
        "User ID", UUID("455b93eb-c78f-4494-9f73-d3291130f126"), unique_files
    )

    assert len(dictionary["User ID"][UUID("455b93eb-c78f-4494-9f73-d3291130f126")]) == 24


def test_get_files_by_account():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    dictionary = files.get_specified_files(
        "Account ID", UUID("73f52be0-368c-42d8-a1fd-660d49ba5604"), unique_files
    )

    assert len(dictionary["Account ID"][UUID("73f52be0-368c-42d8-a1fd-660d49ba5604")]) == 24


def test_get_files_by_serial_number():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "2020_08_04_build_775")
    )

    dictionary = files.get_specified_files("Mantarray Serial Number", "M02001900", unique_files)

    assert len(dictionary["Mantarray Serial Number"]["M02001900"]) == 24


def test_PlateRecording__raises_error_if_files_not_from_same_session(
    generic_well_file, generic_well_file_0_3_1
):
    with pytest.raises(
        WellRecordingsNotFromSameSessionError,
        match=r"'MA20001010'.*2020-08-04 22:01:27.491628\+00:00.*MA20123456.*2020-08-17 14:58:10.728254\+00:00",
    ):
        PlateRecording((generic_well_file.get_file_name(), generic_well_file_0_3_1.get_file_name()))


def test_PlateRecording__can_init_from_filepath_or_wellfile(generic_well_file_0_3_1):
    file_path = os.path.join(
        PATH_OF_CURRENT_FILE,
        "h5",
        "v0.3.1",
        "MA20123456__2020_08_17_145752__B4.h5",
    )
    pr = PlateRecording((file_path, generic_well_file_0_3_1))
    assert len(pr.get_well_names()) == 2


def test_PlateRecording__get_well_by_index__works_when_not_all_wells_present_in_PlateRecording(
    generic_well_file_0_3_1,
):
    pr = PlateRecording([generic_well_file_0_3_1])
    assert pr.get_well_by_index(9) is generic_well_file_0_3_1


def test_PlateRecording__get_well_indices__returns_sorted_set(
    generic_well_file_0_3_1, generic_well_file_0_3_1__2
):
    pr = PlateRecording([generic_well_file_0_3_1, generic_well_file_0_3_1__2])
    assert pr.get_well_indices() == (4, 9)


def test_WellFile__is_backwards_compatible_with_H5_file_v0_1_1():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )

    assert wf.get_h5_attribute(FILE_FORMAT_VERSION_METADATA_KEY) == "0.1.1"
    assert isinstance(wf.get_h5_file(), h5py.File)
    assert "M120171010__2020_07_22_201922__A1" in wf.get_file_name()
    assert wf.get_unique_recording_key() == (
        "M120171010",
        datetime.datetime(2020, 7, 22, 20, 19, 20 + 15, 328587, tzinfo=datetime.timezone.utc),
    )
    assert wf.get_well_name() == "A1"
    assert wf.get_well_index() == 0
    assert wf.get_plate_barcode() == "M120171010"
    assert wf.get_user_account() == UUID("bab42d5a-25ab-4b88-90ca-55914b55cf58")
    assert wf.get_timestamp_of_beginning_of_data_acquisition() == datetime.datetime(
        2020, 7, 22, 20, 19, 20, 328587, tzinfo=datetime.timezone.utc
    )
    assert wf.get_customer_account() == UUID("73f52be0-368c-42d8-a1fd-660d49ba5604")
    assert wf.get_mantarray_serial_number() == "M02001900"
    assert wf.get_begin_recording() == datetime.datetime(
        2020, 7, 22, 20, 19, 20 + 15, 328587, tzinfo=datetime.timezone.utc
    )
    assert wf.get_timestamp_of_first_tissue_data_point() == datetime.datetime(
        2020, 7, 22, 20, 19, 22, 536587, tzinfo=datetime.timezone.utc
    )
    assert wf.get_timestamp_of_first_ref_data_point() == datetime.datetime(
        2020, 7, 22, 20, 19, 22, 530587, tzinfo=datetime.timezone.utc
    )
    assert wf.get_tissue_sampling_period_microseconds() == 9600
    assert wf.get_recording_start_index() == 220000
    assert isinstance(wf.get_raw_tissue_reading(), np.ndarray)


def test_PlateRecording__init__raises_error_if_given_a_file_with_version_v0_1():
    with pytest.raises(
        UnsupportedMantarrayFileVersionError,
        match=f"Mantarray files of version 0.1 are not supported. The minimum supported file version is {MIN_SUPPORTED_FILE_VERSION}",
    ):
        PlateRecording(
            [
                os.path.join(
                    PATH_OF_CURRENT_FILE,
                    "h5",
                    "v0.1",
                    "MA20001100__2020_07_15_172203__A4.h5",
                )
            ]
        )


def test_get_raw_tissue_reading__performance(generic_well_file_0_3_1):
    # start:                        63748857.45
    # remove slow loop:              1382431.61
    # *cache raw tissue reading:       47306.83
    # adding beta 2 support:           59468.82

    num_iterations = 100
    start = time.perf_counter_ns()
    for _ in range(num_iterations):
        generic_well_file_0_3_1.get_raw_tissue_reading()
    dur = time.perf_counter_ns() - start
    dur_per_iter = dur / num_iterations
    # print(dur_per_iter)
    assert dur_per_iter < 10000000


def test_get_raw_reference_reading__performance(generic_well_file_0_3_1):
    # start (see * above):             48397.32
    # adding beta 2 support:           59384.57

    num_iterations = 100
    start = time.perf_counter_ns()
    for _ in range(num_iterations):
        generic_well_file_0_3_1.get_raw_reference_reading()
    dur = time.perf_counter_ns() - start
    dur_per_iter = dur / num_iterations
    # print(dur_per_iter)
    assert dur_per_iter < 10000000


def test_WELL_FILE_CLASSES():
    assert WELL_FILE_CLASSES == immutabledict(
        {"0.3.1": WellFile_0_3_1, "0.4.1": WellFile_0_4_1, "0.4.2": WellFile_0_4_2}
    )
