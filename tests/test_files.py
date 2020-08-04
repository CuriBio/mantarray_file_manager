# -*- coding: utf-8 -*-
import inspect
import os

from mantarray_file_manager import files
from mantarray_file_manager import PlateRecording
from mantarray_file_manager import WellFile
import numpy as np

PATH_OF_CURRENT_FILE = os.path.dirname((inspect.stack()[0][1]))


def test_WellFile__opens_and_get_well_name():
    wf = WellFile(
        os.path.join(PATH_OF_CURRENT_FILE, "h5", "my_barcode__2020_03_17_163600__D6.h5")
    )
    assert wf.get_well_name() == "D6"


def test_WellFile__opens_and_get_well_index():
    wf = WellFile(
        os.path.join(PATH_OF_CURRENT_FILE, "h5", "my_barcode__2020_03_17_163600__D6.h5")
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
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )
    assert wf.get_user_account() == "bab42d5a-25ab-4b88-90ca-55914b55cf58"


def test_WellFile__opens_and_get_customer_account():
    wf = WellFile(
        os.path.join(
            PATH_OF_CURRENT_FILE,
            "M120171010__2020_07_22_201922",
            "M120171010__2020_07_22_201922__A1.h5",
        )
    )
    assert wf.get_customer_account() == "73f52be0-368c-42d8-a1fd-660d49ba5604"


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
            "MA200440001__2020_08_04_210642",
            "MA200440001__2020_08_04_210642__A1.h5",
        )
    )

    assert wf.get_begin_recording() == "2020-08-04 21:06:42.105937"


def test_WellFile__opens_and_get_numpy_array():
    wf = WellFile(
        os.path.join(PATH_OF_CURRENT_FILE, "h5", "my_barcode__2020_03_17_163600__D6.h5")
    )
    assert np.size(wf.get_numpy_array()) == 25986


def test_WellFile__opens_and_get_voltage_array():
    wf = WellFile(
        os.path.join(PATH_OF_CURRENT_FILE, "h5", "my_barcode__2020_03_17_163600__D6.h5")
    )
    assert np.size(wf.get_voltage_array()) == 25986


def test_PlateRecording__opens_and_get_wellfile_names():
    wf1 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B1.h5"
    )
    wf2 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B2.h5"
    )
    wf3 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B3.h5"
    )
    wf4 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B4.h5"
    )
    wf5 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B5.h5"
    )
    wf6 = os.path.join(
        PATH_OF_CURRENT_FILE, "h5_New", "my_barcode__2020_05_24_203716__B6.h5"
    )

    file_list = PlateRecording([wf1, wf2, wf3, wf4, wf5, wf6])

    # test csv writer
    file_list.get_combined_csv()

    assert np.size(file_list.get_wellfile_names()) == 6


def test_get_unique_files():
    unique_files = files.get_unique_files_from_directory(PATH_OF_CURRENT_FILE)

    assert len(unique_files) == 124


def test_get_files_by_well_name():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "h5")
    )

    dictionary = files.get_specified_files("Well Name", "D6", unique_files)

    assert len(dictionary["Well Name"]["D6"]) == 1


def test_get_files_by_plate_barcode():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "M120171010__2020_07_22_201922")
    )

    dictionary = files.get_specified_files("Plate Barcode", "M120171010", unique_files)

    assert len(dictionary["Plate Barcode"]["M120171010"]) == 24


def test_get_files_by_user():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "M120171010__2020_07_22_201922")
    )

    dictionary = files.get_specified_files(
        "User ID", "bab42d5a-25ab-4b88-90ca-55914b55cf58", unique_files
    )

    assert len(dictionary["User ID"]["bab42d5a-25ab-4b88-90ca-55914b55cf58"]) == 24


def test_get_files_by_account():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "M120171010__2020_07_22_201922")
    )

    dictionary = files.get_specified_files(
        "Account ID", "73f52be0-368c-42d8-a1fd-660d49ba5604", unique_files
    )

    assert len(dictionary["Account ID"]["73f52be0-368c-42d8-a1fd-660d49ba5604"]) == 24


def test_get_files_by_serial_number():
    unique_files = files.get_unique_files_from_directory(
        os.path.join(PATH_OF_CURRENT_FILE, "M120171010__2020_07_22_201922")
    )

    dictionary = files.get_specified_files(
        "Mantarray Serial Number", "M02001900", unique_files
    )

    assert len(dictionary["Mantarray Serial Number"]["M02001900"]) == 24
