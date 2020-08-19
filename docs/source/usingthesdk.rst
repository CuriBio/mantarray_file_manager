.. _usingthesdk:

Working With the SDK
======================

In this page there are a list of methods that allow you to use the full functionality of the SDK.

I will briefly descirbe a few of the important ones to get you going:

Getting Metadata
-----------------
 * Make a WellFile instance, for example:
    wf = WellFile(PATH_TO_YOUR_FILE)

 * Use these commands to get certain aspects of your h5 files
    wf.get_file_name()
    wf.get_unique_recording_key()
    wf.get_well_name()
    wf.get_well_index()
    wf.get_plate_barcode()
    wf.get_user_account()
    wf.get_timestamp_of_beginning_of_data_acquisition()
    wf.get_customer_account()
    wf.get_mantarray_serial_number()
    wf.get_begin_recording()
    wf.get_timestamp_of_first_tissue_data_point()
    wf.get_tissue_sampling_period_microseconds()
    
Getting Raw Data
-----------------
 * Make a WellFile instance, for example:
    wf = WellFile(PATH_TO_YOUR_FILE)

 * data = wf.get_raw_tissue_reading()
 
 
Get Arrays of Time vs. Voltage or Time vs. Raw Data
-----------------------------------------------------
 * Make a WellFile instance, for example:
    wf = WellFile(PATH_TO_YOUR_FILE)

 * Voltage vs. Time
    array = wf.get_voltage_array()
    
 * Raw Data vs. Time
    array = wf.get_numpy_array()


Getting a .csv of all desired wells into one
----------------------------------------------
 * Make an instance of a PlateRecording
    pr = PlateRecording([WellFile(FILE_PATH1), WellFile(FILE_PATH2), WellFile(FILE_PATH3), etc.])

 * pr.get_combined_csv() -- will create csv file in the same file path as the Jupyter Notebook being worked in
 




List of all Methods Available to Use
--------------------------------------

.. automodule:: mantarray_file_manager.files
    :members: