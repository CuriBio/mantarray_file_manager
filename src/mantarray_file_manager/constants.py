# -*- coding: utf-8 -*-
"""Constants for the Mantarray File Manager."""
import uuid

from immutabledict import immutabledict

CURI_BIO_ACCOUNT_UUID = uuid.UUID("73f52be0-368c-42d8-a1fd-660d49ba5604")
CURI_BIO_USER_ACCOUNT_ID = uuid.UUID("455b93eb-c78f-4494-9f73-d3291130f126")

MIN_SUPPORTED_FILE_VERSION = "0.1.1"
CURRENT_BETA1_HDF5_FILE_FORMAT_VERSION = "0.4.2"
CURRENT_BETA2_HDF5_FILE_FORMAT_VERSION = "1.0.0"
FILE_FORMAT_VERSION_METADATA_KEY = "File Format Version"
FILE_MIGRATION_PATHS = immutabledict(
    {
        "0.3.1": "0.4.1",
        "0.4.1": "0.4.2",
    }
)

NOT_APPLICABLE_H5_METADATA = uuid.UUID(
    "59d92e00-99d5-4460-9a28-5a1a0fe9aecf"
)  # Eli (1/19/21): H5 files can't store the concept of `None` in their metadata, so using this value to denote that a particular piece of metadata is not available (i.e. after migrating to a newer file format version)

HARDWARE_TEST_RECORDING_UUID = uuid.UUID("a2e76058-08cd-475d-a55d-31d401c3cb34")
UTC_BEGINNING_DATA_ACQUISTION_UUID = uuid.UUID("98c67f22-013b-421a-831b-0ea55df4651e")
START_RECORDING_TIME_INDEX_UUID = uuid.UUID("e41422b3-c903-48fd-9856-46ff56a6534c")
UTC_BEGINNING_RECORDING_UUID = uuid.UUID("d2449271-0e84-4b45-a28b-8deab390b7c2")
UTC_FIRST_TISSUE_DATA_POINT_UUID = uuid.UUID("b32fb8cb-ebf8-4378-a2c0-f53a27bc77cc")
UTC_FIRST_REF_DATA_POINT_UUID = uuid.UUID("7cc07b2b-4146-4374-b8f3-1c4d40ff0cf7")
CUSTOMER_ACCOUNT_ID_UUID = uuid.UUID("4927c810-fbf4-406f-a848-eba5308576e6")
USER_ACCOUNT_ID_UUID = uuid.UUID("7282cf00-2b6e-4202-9d9e-db0c73c3a71f")
SOFTWARE_BUILD_NUMBER_UUID = uuid.UUID("b4db8436-10a4-4359-932d-aa80e6de5c76")
SOFTWARE_RELEASE_VERSION_UUID = uuid.UUID("432fc3c1-051b-4604-bc3d-cc0d0bd75368")
MAIN_FIRMWARE_VERSION_UUID = uuid.UUID("faa48a0c-0155-4234-afbf-5e5dbaa59537")
SLEEP_FIRMWARE_VERSION_UUID = uuid.UUID("3a816076-90e4-4437-9929-dc910724a49d")
XEM_SERIAL_NUMBER_UUID = uuid.UUID("e5f5b134-60c7-4881-a531-33aa0edba540")
MANTARRAY_NICKNAME_UUID = uuid.UUID("0cdec9bb-d2b4-4c5b-9dd5-6a49766c5ed4")
MANTARRAY_SERIAL_NUMBER_UUID = uuid.UUID("83720d36-b941-4d85-9b39-1d817799edd6")
REFERENCE_VOLTAGE_UUID = uuid.UUID("0b3f3f56-0cc7-45f0-b748-9b9de480cba8")
WELL_NAME_UUID = uuid.UUID("6d78f3b9-135a-4195-b014-e74dee70387b")
WELL_ROW_UUID = uuid.UUID("da82fe73-16dd-456a-ac05-0b70fb7e0161")
WELL_COLUMN_UUID = uuid.UUID("7af25a0a-8253-4d32-98c4-3c2ca0d83906")
WELL_INDEX_UUID = uuid.UUID("cd89f639-1e36-4a13-a5ed-7fec6205f779")
TOTAL_WELL_COUNT_UUID = uuid.UUID("7ca73e1c-9555-4eca-8281-3f844b5606dc")
REF_SAMPLING_PERIOD_UUID = uuid.UUID("48aa034d-8775-453f-b135-75a983d6b553")
TISSUE_SAMPLING_PERIOD_UUID = uuid.UUID("f629083a-3724-4100-8ece-c03e637ac19c")
ADC_GAIN_SETTING_UUID = uuid.UUID("a3c3bb32-9b92-4da1-8ed8-6c09f9c816f8")
ADC_TISSUE_OFFSET_UUID = uuid.UUID("41069860-159f-49f2-a59d-401783c1ecb4")
ADC_REF_OFFSET_UUID = uuid.UUID("dc10066c-abf2-42b6-9b94-5e52d1ea9bfc")
PLATE_BARCODE_UUID = uuid.UUID("cf60afef-a9f0-4bc3-89e9-c665c6bb6941")
BACKEND_LOG_UUID = uuid.UUID("87533deb-2495-4430-bce7-12fdfc99158e")
COMPUTER_NAME_HASH_UUID = uuid.UUID("fefd0675-35c2-45f6-855a-9500ad3f100d")
BARCODE_IS_FROM_SCANNER_UUID = uuid.UUID("7d026e86-da70-4464-9181-dc0ce2d47bd1")
IS_FILE_ORIGINAL_UNTRIMMED_UUID = uuid.UUID("52231a24-97a3-497a-917c-86c780d9993f")
TRIMMED_TIME_FROM_ORIGINAL_START_UUID = uuid.UUID("371996e6-5e2d-4183-a5cf-06de7058210a")
TRIMMED_TIME_FROM_ORIGINAL_END_UUID = uuid.UUID("55f6770d-c369-42ce-a437-5ed89c3cb1f8")
ORIGINAL_FILE_VERSION_UUID = uuid.UUID("cd1b4063-4a87-4a57-bc12-923ff4890844")
UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID = uuid.UUID("399b2148-09d4-418b-a132-e37df2721938")
FILE_VERSION_PRIOR_TO_MIGRATION_UUID = uuid.UUID("11b4945b-3cf3-4f67-8bee-7abc3c449756")
BOOTUP_COUNTER_UUID = uuid.UUID("b9ccc724-a39d-429a-be6d-3fd29be5037d")
TOTAL_WORKING_HOURS_UUID = uuid.UUID("f8108718-2fa0-40ce-a51a-8478e5edd4b8")
TAMPER_FLAG_UUID = uuid.UUID("68d0147f-9a84-4423-9c50-228da16ba895")
PCB_SERIAL_NUMBER_UUID = uuid.UUID("5103f995-19d2-4880-8a2e-2ce9080cd2f5")
METADATA_UUID_DESCRIPTIONS = immutabledict(
    {
        # General values
        HARDWARE_TEST_RECORDING_UUID: "Is Hardware Test Recording",
        START_RECORDING_TIME_INDEX_UUID: "Timepoint of Beginning of Recording",
        UTC_BEGINNING_DATA_ACQUISTION_UUID: "UTC Timestamp of Beginning of Data Acquisition",
        UTC_BEGINNING_RECORDING_UUID: "UTC Timestamp of Beginning of Recording",
        UTC_FIRST_TISSUE_DATA_POINT_UUID: "UTC Timestamp of Beginning of Recorded Tissue Sensor Data",
        UTC_FIRST_REF_DATA_POINT_UUID: "UTC Timestamp of Beginning of Recorded Reference Sensor Data",
        CUSTOMER_ACCOUNT_ID_UUID: "Customer Account ID",
        USER_ACCOUNT_ID_UUID: "User Account ID",
        SOFTWARE_BUILD_NUMBER_UUID: "Software Build Number",
        SOFTWARE_RELEASE_VERSION_UUID: "Software Release Version",
        MAIN_FIRMWARE_VERSION_UUID: "Firmware Version (Main Controller)",
        SLEEP_FIRMWARE_VERSION_UUID: "Firmware Version (Sleep Mode)",
        MANTARRAY_NICKNAME_UUID: "Mantarray Nickname",
        MANTARRAY_SERIAL_NUMBER_UUID: "Mantarray Serial Number",
        REFERENCE_VOLTAGE_UUID: "Reference Voltage",
        WELL_NAME_UUID: "Well Name",
        WELL_ROW_UUID: "Well Row (zero-based)",
        WELL_COLUMN_UUID: "Well Column (zero-based)",
        WELL_INDEX_UUID: "Well Index (zero-based)",
        TOTAL_WELL_COUNT_UUID: "Total Wells in Plate",
        REF_SAMPLING_PERIOD_UUID: "Reference Sensor Sampling Period (microseconds)",
        TISSUE_SAMPLING_PERIOD_UUID: "Tissue Sensor Sampling Period (microseconds)",
        ADC_GAIN_SETTING_UUID: "ADC Gain Setting",
        ADC_TISSUE_OFFSET_UUID: "ADC Tissue Sensor Offset",  # may not be needed in Beta 2
        ADC_REF_OFFSET_UUID: "ADC Reference Sensor Offset",  # may not be needed in Beta 2
        PLATE_BARCODE_UUID: "Plate Barcode",
        BACKEND_LOG_UUID: "Backend log file identifier",
        COMPUTER_NAME_HASH_UUID: "SHA512 digest of computer name",
        BARCODE_IS_FROM_SCANNER_UUID: "Is this barcode obtained from the scanner",
        IS_FILE_ORIGINAL_UNTRIMMED_UUID: "Is this an original file straight from the instrument and untrimmed",
        TRIMMED_TIME_FROM_ORIGINAL_START_UUID: "Number of centimilliseconds that has been trimmed off the beginning of when the original data started",
        TRIMMED_TIME_FROM_ORIGINAL_END_UUID: "Number of centimilliseconds that has been trimmed off the end of when the original data ended",
        ORIGINAL_FILE_VERSION_UUID: "The original version of the file when recorded, prior to any migrations to newer versions/formats.",
        UTC_TIMESTAMP_OF_FILE_VERSION_MIGRATION_UUID: "Timestamp when this file was migrated from an earlier version.",
        FILE_VERSION_PRIOR_TO_MIGRATION_UUID: "File format version that this file was migrated from",
        # Beta 1 specific values
        XEM_SERIAL_NUMBER_UUID: "XEM Serial Number",
        # Beta 2 specific values
        BOOTUP_COUNTER_UUID: "The number of times this Mantarray Instrument has booted up",
        TOTAL_WORKING_HOURS_UUID: "The total number of hours this Mantarray Instrument has been powered on and running",
        TAMPER_FLAG_UUID: "Is it suspected the internals of the Mantarray enclosure have been tampered with",
        PCB_SERIAL_NUMBER_UUID: "The serial number of the Mantarray PCB",
    }
)

DATETIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
CENTIMILLISECONDS_PER_SECOND = 1e5
MICROSECONDS_PER_CENTIMILLISECOND = 10
TISSUE_SENSOR_READINGS = "tissue_sensor_readings"
REFERENCE_SENSOR_READINGS = "reference_sensor_readings"
