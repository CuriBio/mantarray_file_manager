# -*- coding: utf-8 -*-
"""Curi Bio File Manager.

File Manager for utilizing Curi bio data files and online databases.
"""
from .constants import ADC_GAIN_SETTING_UUID
from .constants import ADC_REF_OFFSET_UUID
from .constants import ADC_TISSUE_OFFSET_UUID
from .constants import CENTIMILLISECONDS_PER_SECOND
from .constants import CURI_BIO_ACCOUNT_UUID
from .constants import CURI_BIO_USER_ACCOUNT_ID
from .constants import CUSTOMER_ACCOUNT_ID_UUID
from .constants import DATETIME_STR_FORMAT
from .constants import HARDWARE_TEST_RECORDING_UUID
from .constants import MAIN_FIRMWARE_VERSION_UUID
from .constants import MANTARRAY_NICKNAME_UUID
from .constants import MANTARRAY_SERIAL_NUMBER_UUID
from .constants import METADATA_UUID_DESCRIPTIONS
from .constants import MICROSECONDS_PER_CENTIMILLISECOND
from .constants import PLATE_BARCODE_UUID
from .constants import REF_SAMPLING_PERIOD_UUID
from .constants import REFERENCE_VOLTAGE_UUID
from .constants import SLEEP_FIRMWARE_VERSION_UUID
from .constants import SOFTWARE_BUILD_NUMBER_UUID
from .constants import SOFTWARE_RELEASE_VERSION_UUID
from .constants import START_RECORDING_TIME_INDEX_UUID
from .constants import TISSUE_SAMPLING_PERIOD_UUID
from .constants import TOTAL_WELL_COUNT_UUID
from .constants import USER_ACCOUNT_ID_UUID
from .constants import UTC_BEGINNING_DATA_ACQUISTION_UUID
from .constants import UTC_BEGINNING_RECORDING_UUID
from .constants import UTC_FIRST_REF_DATA_POINT_UUID
from .constants import UTC_FIRST_TISSUE_DATA_POINT_UUID
from .constants import WELL_COLUMN_UUID
from .constants import WELL_INDEX_UUID
from .constants import WELL_NAME_UUID
from .constants import WELL_ROW_UUID
from .constants import XEM_SERIAL_NUMBER_UUID
from .exceptions import WellRecordingsNotFromSameSessionError
from .files import PlateRecording
from .files import WellFile

try:  # adapted from https://packaging.python.org/guides/single-sourcing-package-version/
    from importlib import metadata
except ImportError:  # pragma: no cover
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this
__version__: str = metadata.version("mantarray_file_manager")  # type: ignore # Eli (9/1/20): for some reason mypy is giving weird errors for this

__all__ = [
    "WellFile",
    "__version__",
    "PlateRecording",
    "UTC_BEGINNING_DATA_ACQUISTION_UUID",
    "START_RECORDING_TIME_INDEX_UUID",
    "CUSTOMER_ACCOUNT_ID_UUID",
    "USER_ACCOUNT_ID_UUID",
    "SOFTWARE_BUILD_NUMBER_UUID",
    "SOFTWARE_RELEASE_VERSION_UUID",
    "MAIN_FIRMWARE_VERSION_UUID",
    "SLEEP_FIRMWARE_VERSION_UUID",
    "XEM_SERIAL_NUMBER_UUID",
    "MANTARRAY_NICKNAME_UUID",
    "REFERENCE_VOLTAGE_UUID",
    "WELL_NAME_UUID",
    "WELL_ROW_UUID",
    "WELL_COLUMN_UUID",
    "WELL_INDEX_UUID",
    "TOTAL_WELL_COUNT_UUID",
    "REF_SAMPLING_PERIOD_UUID",
    "TISSUE_SAMPLING_PERIOD_UUID",
    "ADC_GAIN_SETTING_UUID",
    "PLATE_BARCODE_UUID",
    "ADC_TISSUE_OFFSET_UUID",
    "ADC_REF_OFFSET_UUID",
    "MANTARRAY_SERIAL_NUMBER_UUID",
    "UTC_BEGINNING_RECORDING_UUID",
    "UTC_FIRST_TISSUE_DATA_POINT_UUID",
    "UTC_FIRST_REF_DATA_POINT_UUID",
    "HARDWARE_TEST_RECORDING_UUID",
    "CURI_BIO_ACCOUNT_UUID",
    "CURI_BIO_USER_ACCOUNT_ID",
    "METADATA_UUID_DESCRIPTIONS",
    "DATETIME_STR_FORMAT",
    "CENTIMILLISECONDS_PER_SECOND",
    "MICROSECONDS_PER_CENTIMILLISECOND",
    "WellRecordingsNotFromSameSessionError",
]
