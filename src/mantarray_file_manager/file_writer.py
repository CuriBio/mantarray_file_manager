# -*- coding: utf-8 -*-
"""Classes and functions for writing and migrating files."""
import datetime
import ntpath
import os
from os import getcwd
from typing import Optional
from typing import Tuple
from typing import Union
import uuid

import h5py

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
from .exceptions import UnsupportedFileMigrationPath
from .files import BasicWellFile
from .files import WELL_FILE_CLASSES


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
