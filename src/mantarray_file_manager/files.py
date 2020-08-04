# -*- coding: utf-8 -*-
"""Classes and functinos for finding and managing files."""
import inspect
import os
from typing import Dict
from typing import List

import h5py
from nptyping import NDArray
import numpy as np

from .constants import CUSTOMER_ACCOUNT_ID_UUID
from .constants import MANTARRAY_SERIAL_NUMBER_UUID
from .constants import PLATE_BARCODE_UUID
from .constants import USER_ACCOUNT_ID_UUID

PATH_OF_CURRENT_FILE = os.path.dirname((inspect.stack()[0][1]))


def get_unique_files_from_directory(directory: str) -> List[str]:
    """Obtain a list of all unique h5 files in the current directory.

    Args:
        directory: the master folder for which all h5 files reside

    Returns:
        A list of the file paths for all the h5 files in the directory.
    """
    unique_files: List[str] = []

    for path, _, files in os.walk(directory):
        for name in files:
            unique_files.append(os.path.join(path, name))

    return unique_files


def get_specified_files(
    search_criteria: str, criteria_value: str, unique_files: List[str]
) -> Dict[str, Dict[str, List[str]]]:
    """Obtain a subset of all the h5 files based on search criteria from user.

    Args:
        search_criteria: A str representing a UUID to a piece a metadata to filter results

    Returns:
        a dictionary of the Plate Recordings that fall under the specified search criteria.
    """
    # unique_files: List[str] = get_unique_files_from_directory(PATH_OF_CURRENT_FILE)

    value_dict: Dict[str, List[str]] = {}
    full_dict: Dict[str, Dict[str, List[str]]] = {}
    plate_recording_list: List[str] = []

    for file in unique_files:
        well = WellFile(file)
        if search_criteria == "Well Name" and well.get_well_name() == criteria_value:
            plate_recording_list.append(file)
        if (
            search_criteria == "Plate Barcode"
            and well.get_plate_barcode() == criteria_value
        ):
            plate_recording_list.append(file)
        if search_criteria == "User ID" and well.get_user_account() == criteria_value:
            plate_recording_list.append(file)
        if (
            search_criteria == "Account ID"
            and well.get_customer_account() == criteria_value
        ):
            plate_recording_list.append(file)
        if (
            search_criteria == "Mantarray Serial Number"
            and well.get_mantarray_serial_number() == criteria_value
        ):
            plate_recording_list.append(file)

    value_dict = {criteria_value: plate_recording_list}
    full_dict = {search_criteria: value_dict}

    return full_dict


class WellFile:
    """Wrapper around an H5 file for a single well of data.

    Args:
        file_name: The path of the H5 file to open.

    Attributes:
        _h5_file: The opened H5 file object.
    """

    def __init__(self, file_name: str) -> None:
        self._h5_file: h5py._hl.files.File = h5py.File(
            file_name, "r",
        )

    def get_well_name(self) -> str:
        return str(self._h5_file.attrs["Well Name"])

    def get_well_index(self) -> int:
        return int(self._h5_file.attrs["Well Index (zero-based)"])

    def get_plate_barcode(self) -> str:
        return str(self._h5_file.attrs[str(PLATE_BARCODE_UUID)])

    def get_user_account(self) -> str:
        return str(self._h5_file.attrs[str(USER_ACCOUNT_ID_UUID)])

    def get_customer_account(self) -> str:
        return str(self._h5_file.attrs[str(CUSTOMER_ACCOUNT_ID_UUID)])

    def get_mantarray_serial_number(self) -> str:
        return str(self._h5_file.attrs[str(MANTARRAY_SERIAL_NUMBER_UUID)])

    # def get_UTC_begin_recording(self) -> str:
    #     return str(self._h5_file.attrs[str(UTC_BEGINNING_RECORDING_UUID)])

    def get_numpy_array(self) -> NDArray[2, float]:
        """Return the data (tissue sensor vs time)."""
        time_step = 8 * 1.2e-3  # tissue sample rate is just over 100Hz
        tissue_data = self._h5_file["tissue_sensor_readings"]

        times = np.arange(len(tissue_data)) * time_step
        len_time = len(times)

        data = np.zeros((2, len_time))
        for i in range(len_time):
            data[0, i] = times[i]
            data[1, i] = tissue_data[i]

        return data

    def get_voltage_array(self) -> NDArray[2, float]:
        """Return the voltage vs time data."""
        time_step = 8 * 1.2e-3  # tissue sample rate is just over 100Hz
        vref = 3.3  # ADC reference voltage
        least_significant_bit = vref / 2 ** 23  # ADC quantization step
        gain = 1  # ADC gain
        tissue_data = self._h5_file["tissue_sensor_readings"]

        times = np.arange(len(tissue_data)) * time_step
        len_time = len(times)

        voltages = []
        for this_tissue_data in tissue_data:
            voltages.append(1e3 * (least_significant_bit * this_tissue_data) / gain)

        voltage_data = np.zeros((2, len_time))
        for i in range(len_time):
            voltage_data[0, i] = times[i]
            voltage_data[1, i] = voltages[i]

        return voltage_data


class PlateRecording:
    """Wrapper around 24 WellFiles fpr a single plate of data.

    Args:
        file_paths: A list of all the file paths for each h5 file to open.

    Attributes:
        _files_ : WellFiles of all the file paths provided.
    """

    def __init__(self, file_paths: List[str]) -> None:
        self._files_: List[str] = file_paths

    def get_wellfile_names(self) -> List[str]:
        well_files = []
        for well in self._files_:
            well_files.append(WellFile(well).get_well_name())
        return well_files

    def get_combined_csv(self) -> None:
        data = np.zeros((len(self._files_) + 1, 12315))
        for i, well in enumerate(self._files_):
            well_data = WellFile(well).get_numpy_array()
            data[0, :] = well_data[0, :]
            data[i + 1, :] = well_data[1, :]

        my_local_path_data = os.path.join(PATH_OF_CURRENT_FILE, "PlateRecording.csv")
        np.savetxt(my_local_path_data, data, delimiter=",", fmt="%d")
