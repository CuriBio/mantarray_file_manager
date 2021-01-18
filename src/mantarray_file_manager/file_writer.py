# -*- coding: utf-8 -*-
"""Classes and functions for writing and migrating files."""
import h5py

from .constants import CURRENT_HDF5_FILE_FORMAT_VERSION
from .constants import FILE_MIGRATION_PATHS
from .exceptions import UnsupportedFileMigrationPath
from .files import BasicWellFile


class MantarrayH5FileCreator(
    h5py.File
):  # pylint: disable=too-many-ancestors # Eli (7/28/20): I don't see a way around this...we need to subclass h5py File
    """Creates an H5 file with the basic format/layout."""

    def __init__(self, file_name: str) -> None:
        super().__init__(
            file_name,
            "w",
            libver="latest",  # Eli (2/9/20) tried to specify this ('earliest', 'v110') to be more backward compatible but it didn't work for unknown reasons (gave error when trying to set swmr_mode=True)
            userblock_size=512,  # minimum size is 512 bytes
        )

        self.attrs["File Format Version"] = CURRENT_HDF5_FILE_FORMAT_VERSION


def migrate_to_latest_version(
    starting_file_path: str,  # , working_directory: Optional[str] = None
) -> str:
    """Migrates an H5 file to the latest version.

    Args:
        starting_file_path: the path to the H5 file
        working_directory: the directory in which to create the new files. Defaults to current working directory

    Returns:
        The path to the final H5 file migrated to the latest version.
    """
    file = BasicWellFile(starting_file_path)
    file_version = file.get_file_version()
    if file_version == CURRENT_HDF5_FILE_FORMAT_VERSION:
        return starting_file_path
    if file_version not in FILE_MIGRATION_PATHS:
        raise UnsupportedFileMigrationPath(file_version)
    return starting_file_path
