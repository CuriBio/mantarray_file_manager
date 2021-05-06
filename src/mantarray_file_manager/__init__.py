# -*- coding: utf-8 -*-
"""Curi Bio File Manager.

File Manager for utilizing Curi bio data files and online databases.
"""
from . import file_writer
from .constants import ADC_GAIN_SETTING_UUID
from .constants import ADC_REF_OFFSET_UUID
from .constants import ADC_TISSUE_OFFSET_UUID
from .constants import BACKEND_LOG_UUID
from .constants import BARCODE_IS_FROM_SCANNER_UUID
from .constants import BOOTUP_COUNTER_UUID
from .constants import CENTIMILLISECONDS_PER_SECOND
from .constants import COMPUTER_NAME_HASH_UUID
from .constants import CURI_BIO_ACCOUNT_UUID
from .constants import CURI_BIO_USER_ACCOUNT_ID
from .constants import CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION
from .constants import CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION
from .constants import CUSTOMER_ACCOUNT_ID_UUID
from .constants import DATETIME_STR_FORMAT
from .constants import FILE_FORMAT_VERSION_METADATA_KEY
from .constants import FILE_MIGRATION_PATHS
from .constants import FILE_VERSION_PRIOR_TO_MIGRATION_UUID
from .constants import HARDWARE_TEST_RECORDING_UUID
from .constants import IS_FILE_ORIGINAL_UNTRIMMED_UUID
from .constants import MAIN_FIRMWARE_VERSION_UUID
from .constants import MANTARRAY_NICKNAME_UUID
from .constants import MANTARRAY_SERIAL_NUMBER_UUID
from .constants import METADATA_UUID_DESCRIPTIONS
from .constants import MICROSECONDS_PER_CENTIMILLISECOND
from .constants import MIN_SUPPORTED_FILE_VERSION
from .constants import NOT_APPLICABLE_H5_METADATA
from .constants import ORIGINAL_FILE_VERSION_UUID
from .constants import PCB_SERIAL_NUMBER_UUID
from .constants import PLATE_BARCODE_UUID
from .constants import REF_SAMPLING_PERIOD_UUID
from .constants import REFERENCE_SENSOR_READINGS
from .constants import REFERENCE_VOLTAGE_UUID
from .constants import SLEEP_FIRMWARE_VERSION_UUID
from .constants import SOFTWARE_BUILD_NUMBER_UUID
from .constants import SOFTWARE_RELEASE_VERSION_UUID
from .constants import START_RECORDING_TIME_INDEX_UUID
from .constants import TAMPER_FLAG_UUID
from .constants import TISSUE_SAMPLING_PERIOD_UUID
from .constants import TISSUE_SENSOR_READINGS
from .constants import TOTAL_WELL_COUNT_UUID
from .constants import TOTAL_WORKING_HOURS_UUID
from .constants import TRIMMED_TIME_FROM_ORIGINAL_END_UUID
from .constants import TRIMMED_TIME_FROM_ORIGINAL_START_UUID
from .constants import USER_ACCOUNT_ID_UUID
from .constants import UTC_BEGINNING_DATA_ACQUISTION_UUID
from .constants import UTC_BEGINNING_RECORDING_UUID
from .constants import UTC_FIRST_REF_DATA_POINT_UUID
from .constants import UTC_FIRST_TISSUE_DATA_POINT_UUID
from .constants import UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID
from .constants import WELL_COLUMN_UUID
from .constants import WELL_INDEX_UUID
from .constants import WELL_NAME_UUID
from .constants import WELL_ROW_UUID
from .constants import XEM_SERIAL_NUMBER_UUID
from .exceptions import FileAttributeNotFoundError
from .exceptions import MantarrayFileNotLatestVersionError
from .exceptions import UnsupportedFileMigrationPath
from .exceptions import UnsupportedMantarrayFileVersionError
from .exceptions import WellRecordingsNotFromSameSessionError
from .file_writer import MantarrayH5FileCreator
from .file_writer import migrate_to_latest_version
from .file_writer import migrate_to_next_version
from .files import BasicWellFile
from .files import PlateRecording
from .files import WELL_FILE_CLASSES
from .files import WellFile
from .files import WellFile_0_3_1
from .files import WellFile_0_4_1
from .files import WellFile_0_4_2


__all__ = [
    "WellFile",
    "PlateRecording",
    "UTC_BEGINNING_DATA_ACQUISTION_UUID",
    "FILE_FORMAT_VERSION_METADATA_KEY",
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
    "MIN_SUPPORTED_FILE_VERSION",
    "UnsupportedMantarrayFileVersionError",
    "FileAttributeNotFoundError",
    "BACKEND_LOG_UUID",
    "COMPUTER_NAME_HASH_UUID",
    "BARCODE_IS_FROM_SCANNER_UUID",
    "IS_FILE_ORIGINAL_UNTRIMMED_UUID",
    "TRIMMED_TIME_FROM_ORIGINAL_START_UUID",
    "TRIMMED_TIME_FROM_ORIGINAL_END_UUID",
    "ORIGINAL_FILE_VERSION_UUID",
    "CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION",
    "MantarrayH5FileCreator",
    "FILE_MIGRATION_PATHS",
    "migrate_to_next_version",
    "migrate_to_latest_version",
    "UnsupportedFileMigrationPath",
    "BasicWellFile",
    "WellFile_0_4_1",
    "WellFile_0_3_1",
    "WellFile_0_4_2",
    "file_writer",
    "WELL_FILE_CLASSES",
    "UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID",
    "FILE_VERSION_PRIOR_TO_MIGRATION_UUID",
    "NOT_APPLICABLE_H5_METADATA",
    "MantarrayFileNotLatestVersionError",
    "TISSUE_SENSOR_READINGS",
    "REFERENCE_SENSOR_READINGS",
    "BOOTUP_COUNTER_UUID",
    "TOTAL_WORKING_HOURS_UUID",
    "TAMPER_FLAG_UUID",
    "PCB_SERIAL_NUMBER_UUID",
    "CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION",
]
