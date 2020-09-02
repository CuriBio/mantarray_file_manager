# -*- coding: utf-8 -*-
"""Classes and functinos for finding and managing files."""
import datetime
from glob import glob
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union
from uuid import UUID

import h5py
from nptyping import NDArray
import numpy as np
from stdlib_utils import get_current_file_abs_directory

from .constants import CUSTOMER_ACCOUNT_ID_UUID
from .constants import DATETIME_STR_FORMAT
from .constants import MANTARRAY_SERIAL_NUMBER_UUID
from .constants import MICROSECONDS_PER_CENTIMILLISECOND
from .constants import PLATE_BARCODE_UUID
from .constants import START_RECORDING_TIME_INDEX_UUID
from .constants import TISSUE_SAMPLING_PERIOD_UUID
from .constants import USER_ACCOUNT_ID_UUID
from .constants import UTC_BEGINNING_DATA_ACQUISTION_UUID
from .constants import UTC_BEGINNING_RECORDING_UUID
from .constants import UTC_FIRST_TISSUE_DATA_POINT_UUID
from .constants import WELL_INDEX_UUID
from .constants import WELL_NAME_UUID
from .exceptions import WellRecordingsNotFromSameSessionError

PATH_OF_CURRENT_FILE = get_current_file_abs_directory()


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
            if name.endswith(".h5"):
                unique_files.append(os.path.join(path, name))

    for file in unique_files:
        well = WellFile(file)
        index = well.get_well_index()
        barcode = well.get_plate_barcode()
        start_time = well.get_begin_recording()

        duplicates = []

        unique_files.remove(file)

        for item in unique_files:
            new_well = WellFile(item)
            if (
                new_well.get_well_index() == index
                and new_well.get_plate_barcode() == barcode
                and new_well.get_begin_recording() == start_time
            ):
                duplicates.append(item)

        unique_files.append(file)

        for duplicate_file in duplicates:
            unique_files.remove(duplicate_file)

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


def _extract_datetime_from_h5(
    open_h5_file: h5py._hl.files.File,  # pylint: disable=protected-access # WTF pylint...this is a type definition
    metadata_uuid: UUID,
) -> datetime.datetime:
    timestamp_str = open_h5_file.attrs[str(metadata_uuid)]
    return datetime.datetime.strptime(timestamp_str, DATETIME_STR_FORMAT).replace(
        tzinfo=datetime.timezone.utc
    )


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
        self._file_name = file_name

    def get_h5_file(
        self,
    ) -> h5py._hl.files.File:  # pylint: disable=protected-access # WTF pylint...this is a type definition
        return self._h5_file

    def get_file_name(self) -> str:
        return self._file_name

    def get_unique_recording_key(self) -> Tuple[str, datetime.datetime]:
        barcode = self.get_plate_barcode()
        start_time = self.get_begin_recording()
        return barcode, start_time

    def get_h5_attribute(self, attr_name: str) -> Any:
        return self._h5_file.attrs[attr_name]

    def get_well_name(self) -> str:
        return str(self._h5_file.attrs[str(WELL_NAME_UUID)])

    def get_well_index(self) -> int:
        return int(self._h5_file.attrs[str(WELL_INDEX_UUID)])

    def get_plate_barcode(self) -> str:
        return str(self._h5_file.attrs[str(PLATE_BARCODE_UUID)])

    def get_user_account(self) -> UUID:
        return UUID(self._h5_file.attrs[str(USER_ACCOUNT_ID_UUID)])

    def get_timestamp_of_beginning_of_data_acquisition(self) -> datetime.datetime:
        return _extract_datetime_from_h5(
            self._h5_file, UTC_BEGINNING_DATA_ACQUISTION_UUID
        )

    def get_customer_account(self) -> UUID:
        return UUID(self._h5_file.attrs[str(CUSTOMER_ACCOUNT_ID_UUID)])

    def get_mantarray_serial_number(self) -> str:
        return str(self._h5_file.attrs[str(MANTARRAY_SERIAL_NUMBER_UUID)])

    def get_begin_recording(self) -> datetime.datetime:
        return _extract_datetime_from_h5(self._h5_file, UTC_BEGINNING_RECORDING_UUID)

    def get_timestamp_of_first_tissue_data_point(self) -> datetime.datetime:
        return _extract_datetime_from_h5(
            self._h5_file, UTC_FIRST_TISSUE_DATA_POINT_UUID
        )

    def get_tissue_sampling_period_microseconds(self) -> int:
        return int(self._h5_file.attrs[str(TISSUE_SAMPLING_PERIOD_UUID)])

    def get_recording_start_index(self) -> int:
        """Get the time index when recording was requested.

        This is the number of centimilliseconds from beginning of the
        start of data acquisition that was displayed on the screen when
        the user pressed the Record button.
        """
        return int(self._h5_file.attrs[str(START_RECORDING_TIME_INDEX_UUID)])

    def get_raw_tissue_reading(self) -> NDArray[(2, Any), int]:
        """Get a value vs time array.

        Time (centi-milliseconds) is first dimension, value is second
        dimension.

        Time is given relative to the start of the recording, so that arrays from different wells can be displayed together
        """
        recording_start_index_useconds = (
            self.get_recording_start_index() * MICROSECONDS_PER_CENTIMILLISECOND
        )
        timestamp_of_start_index = self.get_timestamp_of_beginning_of_data_acquisition() + datetime.timedelta(
            microseconds=recording_start_index_useconds
        )
        time_delta = (
            self.get_timestamp_of_first_tissue_data_point() - timestamp_of_start_index
        )

        time_delta_centimilliseconds = int(
            time_delta
            / datetime.timedelta(microseconds=MICROSECONDS_PER_CENTIMILLISECOND)
        )

        time_step = int(
            self.get_tissue_sampling_period_microseconds()
            / MICROSECONDS_PER_CENTIMILLISECOND
        )
        tissue_data = self._h5_file["tissue_sensor_readings"]

        times = np.arange(len(tissue_data), dtype=np.int32) * time_step
        len_time = len(times)

        data = np.zeros((2, len_time), dtype=np.int32)
        for i in range(len_time):
            data[0, i] = times[i] + time_delta_centimilliseconds
            data[1, i] = tissue_data[i]

        return data

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
        file_paths: A list of all the file paths for each h5 file to open, or already instantiated WellFile objects.

    Attributes:
        _files : WellFiles of all the file paths provided.
    """

    def __init__(self, file_paths: Sequence[Union[str, WellFile]]) -> None:
        self._files: List[WellFile] = list()
        self._wells_by_index: Dict[int, WellFile] = dict()
        for iter_file_path in file_paths:

            well_file = iter_file_path
            if isinstance(well_file, str):
                well_file = WellFile(well_file)
            if len(self._files) > 0:
                new_session_key = well_file.get_unique_recording_key()
                old_file = self._files[0]
                old_session_key = old_file.get_unique_recording_key()
                if new_session_key != old_session_key:
                    raise WellRecordingsNotFromSameSessionError(old_file, well_file)
            self._files.append(well_file)
            self._wells_by_index[well_file.get_well_index()] = well_file

    @classmethod
    def from_directory(cls, dir_to_load_files_from: str) -> "PlateRecording":
        return cls(glob(os.path.join(dir_to_load_files_from, "*.h5")))

    def get_well_by_index(self, well_index: int) -> WellFile:
        return self._wells_by_index[well_index]

    def get_wellfile_names(self) -> Sequence[str]:
        well_files = []
        for well in self._files:
            well_files.append(well.get_well_name())
        return well_files

    def get_well_names(self) -> Set[str]:
        out_set: Set[str] = set()
        for iter_well_file in self._files:
            out_set.add(iter_well_file.get_well_name())
        return out_set

    def get_well_indices(self) -> Tuple[int, ...]:
        return tuple(sorted(self._wells_by_index.keys()))

    def get_combined_csv(self) -> None:
        data = np.zeros((len(self._files) + 1, 5495))
        for i, well in enumerate(self._files):
            well_data = well.get_numpy_array()
            data[0, :] = well_data[0, 0:5495]
            data[i + 1, :] = well_data[1, 0:5495]

        my_local_path_data = os.path.join(PATH_OF_CURRENT_FILE, "PlateRecording.csv")
        np.savetxt(my_local_path_data, data, delimiter=",", fmt="%d")
