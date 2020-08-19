# -*- coding: utf-8 -*-
"""Exceptions."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .files import WellFile


class WellRecordingsNotFromSameSessionError(Exception):
    def __init__(self, main_well_file: "WellFile", new_well_file: "WellFile"):
        super().__init__(
            f"Previously loaded files for this Plate Recording session were from barcode '{main_well_file.get_plate_barcode()}' taken at {main_well_file.get_begin_recording()}. A new file is attempting to be added that is from barcode '{new_well_file.get_plate_barcode()}' taken at {new_well_file.get_begin_recording()}"
        )
