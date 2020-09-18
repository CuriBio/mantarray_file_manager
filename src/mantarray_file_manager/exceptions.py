# -*- coding: utf-8 -*-
"""Exceptions."""
from typing import TYPE_CHECKING

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
    def __init__(
        self, attr_name: str, file_version: str, file_path: str,
    ):
        super().__init__(
            f"The metadata attribute {attr_name} was not found in this file. File format version {file_version}, filepath: {file_path}"
        )
