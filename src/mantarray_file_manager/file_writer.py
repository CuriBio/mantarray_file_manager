# -*- coding: utf-8 -*-
"""Classes and functions for writing and migrating files."""
import h5py

from .constants import CURRENT_HDF5_FILE_FORMAT_VERSION


class MantarrayH5FileCreator(
    h5py.File
):  # pylint: disable=too-many-ancestors # Eli (7/28/20): I don't see a way around this...we need to subclass h5py File
    def __init__(self, file_name: str) -> None:
        super().__init__(
            file_name,
            "w",
            libver="latest",  # Eli (2/9/20) tried to specify this ('earliest', 'v110') to be more backward compatible but it didn't work for unknown reasons (gave error when trying to set swmr_mode=True)
            userblock_size=512,  # minimum size is 512 bytes
        )

        self.attrs["File Format Version"] = CURRENT_HDF5_FILE_FORMAT_VERSION
