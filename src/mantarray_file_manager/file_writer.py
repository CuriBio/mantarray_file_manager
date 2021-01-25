# -*- coding: utf-8 -*-
"""Classes and functions for writing and migrating files."""
import datetime
import ntpath
import os
from os import getcwd
from typing import Any
from typing import Optional
from typing import Tuple
from typing import Union
import uuid

import h5py
from immutable_data_validation.wrapped_vc_validators import validate_int
from nptyping import NDArray
import numpy as np

from .constants import BACKEND_LOG_UUID
from .constants import BARCODE_IS_FROM_SCANNER_UUID
from .constants import COMPUTER_NAME_HASH_UUID
from .constants import CURRENT_HDF5_FILE_FORMAT_VERSION
from .constants import DATETIME_STR_FORMAT
from .constants import FILE_FORMAT_VERSION_METADATA_KEY
from .constants import FILE_MIGRATION_PATHS
from .constants import FILE_VERSION_PRIOR_TO_MIGRATION_UUID
from .constants import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from .constants import NOT_APPLICABLE_H5_METADATA
from .constants import ORIGINAL_FILE_VERSION_UUID
from .constants import TRIMMED_TIME_FROM_ORIGINAL_END_UUID
from .constants import TRIMMED_TIME_FROM_ORIGINAL_START_UUID
from .constants import UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID
from .exceptions import TooTrimmedError
from .exceptions import UnsupportedArgumentError
from .exceptions import UnsupportedFileMigrationPath
from .files import BasicWellFile
from .files import WELL_FILE_CLASSES
from .files import WellFile

np.set_printoptions(edgeitems=10)


class MantarrayH5FileCreator(
    h5py.File
):  # pylint: disable=too-many-ancestors # Eli (7/28/20): I don't see a way around this...we need to subclass h5py File
    """Creates an H5 file with the basic format/layout."""

    def __init__(
        self,
        file_name: str,
        file_format_version: str = CURRENT_HDF5_FILE_FORMAT_VERSION,
    ) -> None:
        super().__init__(
            file_name,
            "w",
            libver="latest",  # Eli (2/9/20) tried to specify this ('earliest', 'v110') to be more backward compatible but it didn't work for unknown reasons (gave error when trying to set swmr_mode=True)
            userblock_size=512,  # minimum size is 512 bytes
        )

        self.attrs[FILE_FORMAT_VERSION_METADATA_KEY] = file_format_version


def _get_format_version_of_file(file_path: str) -> str:
    file = BasicWellFile(file_path)
    file_version = file.get_file_version()
    file.get_h5_file().close()
    return file_version


def migrate_to_next_version(
    starting_file_path: str, working_directory: Optional[str] = None
) -> str:
    """Migrates an H5 file to the next version along the migration path.

    Args:
        starting_file_path: the path to the H5 file
        working_directory: the directory in which to create the new files. Defaults to current working directory

    Returns:
        The path to the H5 file migrated to the next version.
    """
    file_version = _get_format_version_of_file(starting_file_path)
    if file_version == CURRENT_HDF5_FILE_FORMAT_VERSION:
        return starting_file_path
    if working_directory is None:
        working_directory = getcwd()
    if file_version not in FILE_MIGRATION_PATHS:
        raise UnsupportedFileMigrationPath(file_version)
    old_file = WELL_FILE_CLASSES[file_version](starting_file_path)
    new_file_version = FILE_MIGRATION_PATHS[file_version]
    old_file_basename = ntpath.basename(starting_file_path)
    old_file_basename_no_suffix = old_file_basename[:-3]

    new_file_name = os.path.join(
        working_directory, f"{old_file_basename_no_suffix}__v{new_file_version}.h5"
    )
    new_file = MantarrayH5FileCreator(
        new_file_name, file_format_version=new_file_version
    )

    # old metadata
    old_h5_file = old_file.get_h5_file()
    old_metadata_keys = set(old_h5_file.attrs.keys())
    old_metadata_keys.remove(FILE_FORMAT_VERSION_METADATA_KEY)
    for iter_metadata_key in old_metadata_keys:
        new_file.attrs[iter_metadata_key] = old_h5_file.attrs[iter_metadata_key]

    # transfer data
    old_tissue_data = old_h5_file["tissue_sensor_readings"]
    new_file.create_dataset("tissue_sensor_readings", data=old_tissue_data)
    old_reference_data = old_h5_file["reference_sensor_readings"]
    new_file.create_dataset("reference_sensor_readings", data=old_reference_data)

    # new metadata
    metadata_to_create: Tuple[Tuple[uuid.UUID, Union[str, bool, int, float]], ...]
    if new_file_version == "0.4.1":
        metadata_to_create = (
            (BARCODE_IS_FROM_SCANNER_UUID, False),
            (IS_FILE_ORIGINAL_UNTRIMMED_UUID, True),
            (TRIMMED_TIME_FROM_ORIGINAL_START_UUID, 0),
            (TRIMMED_TIME_FROM_ORIGINAL_END_UUID, 0),
            (BACKEND_LOG_UUID, str(NOT_APPLICABLE_H5_METADATA)),
            (COMPUTER_NAME_HASH_UUID, str(NOT_APPLICABLE_H5_METADATA)),
        )
    elif new_file_version == "0.4.2":
        utc_now = datetime.datetime.utcnow()
        formatted_time = utc_now.strftime(DATETIME_STR_FORMAT)
        metadata_to_create = (
            (
                ORIGINAL_FILE_VERSION_UUID,
                str(NOT_APPLICABLE_H5_METADATA),
            ),  # Eli (1/19/21): there's no way I can think of to know for sure what the very original file version was since it wasn't recorded as metadata, so just leaving it blank for now.
            (FILE_VERSION_PRIOR_TO_MIGRATION_UUID, file_version),
            (UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID, formatted_time),
        )
    else:
        raise NotImplementedError(
            f"Migrating to the version {new_file_version} is not supported."
        )
    for iter_metadata_key, iter_metadata_value in metadata_to_create:
        new_file.attrs[str(iter_metadata_key)] = iter_metadata_value

    new_file.close()
    return new_file_name


def migrate_to_latest_version(
    starting_file_path: str, working_directory: Optional[str] = None
) -> str:
    """Migrates an H5 file to the latest version.

    To use from the command line: `python -c "from mantarray_file_manager import migrate_to_latest_version; migrate_to_latest_version('tests/h5/v0.3.1/MA20123456__2020_08_17_145752__A1.h5')"`

    Args:
        starting_file_path: the path to the H5 file
        working_directory: the directory in which to create the new files. Defaults to current working directory

    Returns:
        The path to the final H5 file migrated to the latest version.
    """
    current_file_path = starting_file_path
    while True:
        file_version = _get_format_version_of_file(current_file_path)
        if file_version == CURRENT_HDF5_FILE_FORMAT_VERSION:
            return current_file_path
        current_file_path = migrate_to_next_version(
            current_file_path, working_directory=working_directory
        )


def h5_file_trimmer(
    file_path: str,
    from_start: int,
    from_end: int,
) -> str:
    """Trims an H5 file.

    Args:
        file_path: path to the H5 file
        from_start: centimilliseconds to trim from the start
        from_end: centimilliseconds to trim from the end

    Returns:
        The path to the trimmed H5 file.
    """
    validate_int(
        value=from_start,
        allow_null=True,
        minimum=0,
    )
    validate_int(value=from_end, allow_null=True, minimum=0)
    if not from_start and not from_end:
        raise UnsupportedArgumentError()

    working_directory = getcwd()
    old_file = WellFile(file_path)

    old_file_basename = ntpath.basename(file_path)
    old_file_basename_no_suffix = old_file_basename[:-3]

    # add os.path.join
    new_file_name = os.path.join(
        working_directory,
        f"{old_file_basename_no_suffix}__trimmed_{from_start}_{from_end}.h5",
    )

    new_file = MantarrayH5FileCreator(new_file_name)

    # old metadata
    old_h5_file = old_file.get_h5_file()
    old_metadata_keys = set(old_h5_file.attrs.keys())
    old_from_end = 0

    if str(IS_FILE_ORIGINAL_UNTRIMMED_UUID) in old_metadata_keys:
        old_from_start = old_h5_file.attrs[str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID)]
        old_from_end = old_h5_file.attrs[str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID)]
        old_metadata_keys.remove(str(TRIMMED_TIME_FROM_ORIGINAL_START_UUID))
        old_metadata_keys.remove(str(TRIMMED_TIME_FROM_ORIGINAL_END_UUID))
        old_metadata_keys.remove(str(IS_FILE_ORIGINAL_UNTRIMMED_UUID))
        from_start += old_from_start

    for iter_metadata_key in old_metadata_keys:
        new_file.attrs[iter_metadata_key] = old_h5_file.attrs[iter_metadata_key]

    # new metadata
    metadata_to_create: Tuple[Tuple[uuid.UUID, Union[str, bool, int, float]], ...]

    metadata_to_create = (
        (IS_FILE_ORIGINAL_UNTRIMMED_UUID, False),
        (TRIMMED_TIME_FROM_ORIGINAL_START_UUID, from_start),
        (TRIMMED_TIME_FROM_ORIGINAL_END_UUID, from_end + old_from_end),
    )

    for iter_metadata_key, iter_metadata_value in metadata_to_create:
        new_file.attrs[str(iter_metadata_key)] = iter_metadata_value

    # transfer data
    old_raw_reference_data = old_file.get_raw_reference_reading()
    old_tissue_data = old_file.get_raw_tissue_reading()

    tissue_data_start_index = _find_start_index(from_start, old_tissue_data)
    tissue_data_last_index = _find_last_index(from_end, old_tissue_data)

    reference_data_start_index = _find_start_index(from_start, old_raw_reference_data)
    reference_data_last_index = _find_last_index(
        from_end, old_raw_reference_data
    )  # TODO: need to change this

    if (
        reference_data_start_index >= reference_data_last_index
        or tissue_data_start_index >= tissue_data_last_index
    ):
        raise TooTrimmedError(from_start, from_end)

    new_tissue_sensor_data = old_h5_file["tissue_sensor_readings"]
    new_tissue_sensor_data = np.array(new_tissue_sensor_data)
    new_tissue_sensor_data = new_tissue_sensor_data[
        tissue_data_start_index : tissue_data_last_index + 1
    ]  # +1 because needs to be inclusive of last index

    new_reference_sensor_data = old_h5_file["reference_sensor_readings"]
    new_reference_sensor_data = np.array(new_reference_sensor_data)
    new_reference_sensor_data = new_reference_sensor_data[
        reference_data_start_index : reference_data_last_index + 1
    ]  # +1 because needs to be indclusive of last index

    new_file.create_dataset("tissue_sensor_readings", data=new_tissue_sensor_data)
    new_file.create_dataset("reference_sensor_readings", data=new_reference_sensor_data)

    new_file.close()
    return new_file_name


def _find_start_index(from_start: int, old_data: NDArray[(2, Any), int]) -> int:
    start_index = 0
    if from_start > old_data[0][start_index]:
        while start_index < len(old_data[0]) and from_start >= old_data[0][start_index]:
            start_index = start_index + 1
        start_index = start_index - 1
    return start_index


def _find_last_index(from_end: int, old_data: NDArray[(2, Any), int]) -> int:
    last_index = len(old_data[0]) - 1
    time_elapsed = 0
    if from_end > time_elapsed:
        while last_index > 0 and from_end >= time_elapsed:
            time_elapsed += old_data[0][last_index] - old_data[0][last_index - 1]
            last_index -= 1
        last_index += 1
    return last_index
