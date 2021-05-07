# -*- coding: utf-8 -*-
"""Exceptions."""
from typing import TYPE_CHECKING
from uuid import UUID

from immutable_data_validation import is_uuid
from semver import VersionInfo

from .constants import CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
from .constants import CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION
from .constants import FILE_MIGRATION_PATHS
from .constants import METADATA_UUID_DESCRIPTIONS
from .constants import MIN_SUPPORTED_FILE_VERSION

if TYPE_CHECKING:
    from .files import WellFile


class WellRecordingsNotFromSameSessionError(Exception):
    def __init__(self, main_well_file: "WellFile", new_well_file: "WellFile"):
        super().__init__(
            f"Previously loaded files for this Plate Recording session were from barcode '{main_well_file.get_plate_barcode()}' taken at {main_well_file.get_begin_recording()}. A new file is attempting to be added that is from barcode '{new_well_file.get_plate_barcode()}' taken at {new_well_file.get_begin_recording()}"
        )


class UnsupportedMantarrayFileVersionError(Exception):
    def __init__(self, file_version: str):
        super().__init__(
            f"Mantarray files of version {file_version} are not supported. The minimum supported file version is {MIN_SUPPORTED_FILE_VERSION}"
        )


class FileAttributeNotFoundError(Exception):
    """Error raised if attempting to access a non-existent attribute."""

    def __init__(
        self,
        attr_name: str,
        file_version: str,
        file_path: str,
    ):
        try:
            attr_description = (
                f"{attr_name}, ({METADATA_UUID_DESCRIPTIONS[UUID(attr_name)]})"
                if is_uuid(attr_name)
                else f"{attr_name} (no UUID given)"
            )
        except KeyError:
            attr_description = f"{attr_name} (Unrecognized UUID)"
        super().__init__(
            f"The metadata attribute '{attr_description}' was not found in this file. File format version {file_version}, filepath: {file_path}"
        )


class UnsupportedFileMigrationPath(Exception):
    """Error raised if a file is attempted to be migrated from a version that has no migration script."""

    def __init__(self, file_version: str):
        super().__init__(
            f"There is no supported migration path from version {file_version}. Supported paths are: {FILE_MIGRATION_PATHS}."
        )


class UnsupportedArgumentError(Exception):
    """Error raised if the arguments indicating the amount of centimilliseconds to be trimmed from the start and end are both None."""

    def __init__(self) -> None:
        super().__init__("Both arguments cannot be None or 0.")


class TooTrimmedError(Exception):
    def __init__(self, from_start: int, from_end: int, total_time: int) -> None:
        super().__init__(
            f"When trimming {from_start} centimilliseconds from the start and {from_end} centimilliseconds from the end, the length of the recording is exceeded. The length of the recording is {total_time} centimilliseconds"
        )


class MantarrayFileNotLatestVersionError(Exception):
    """Error raised when a function requiring the latest file format for a specific instrument version is given an old file format."""

    def __init__(self, file_version: str):
        is_beta_1_file = file_version.split(".") < VersionInfo.parse(
            CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION
        )
        latest_file_version = (
            CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
            if is_beta_1_file
            else CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION
        )
        file_type = "Beta 1" if is_beta_1_file else "Beta 2"
        super().__init__(
            f"Mantarray {file_type} files of version {file_version} are not supported. Please migrate to the latest file version for Mantarray {file_type} data: {latest_file_version}"
        )
