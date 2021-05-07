Changelog for Mantarray File Manager
====================================


0.5.0 (2021-05-07)
------------------

- Added support for Beta 2 H5 files.
- Added initial Beta 2 file version 1.0.0.


0.4.8 (2021-04-08)
------------------

- Added the following UUIDs related to the Mantarray Beta 2 metadata:

  - Boot-up counter
  - Total working hours
  - Tamper flag
  - PCB serial number


0.4.6 (2021-02-05)
------------------

- Added file migration function to go from v0.3.1 to v0.4.1 and v0.4.1 to v0.4.2.
- Bumped H5 File version to 0.4.2.
- Added metadata for original file version from Mantarray, file version prior to
  migration, and time migration was performed.
- Added function ``h5_file_trimmer`` to trim h5 files by indicating the amount of
  centimilliseconds to be trimmed from the start and end.


0.4.5 (2021-01-13)
------------------

- Added UUID indicating whether or not this is an original (untrimmed) file.
- Added UUIDs to track the amount of time trimmed from the file (if trimmed).


0.4.4 (2021-01-07)
------------------

- Added UUID indicating whether or not a barcode was obtained via a
  barcode scanner.


0.4.3 (2020-11-16)
------------------

- Added UUIDs for Backend log file identifier and
  SHA512 digest of computer name.


0.4.2 (2020-11-10)
------------------

- Added raw UUID to FileAttributeNotFoundError if one is given.


0.4.1 (2020-10-05)
------------------

- Fixed compatibility with H5 files of v0.1.1.


0.4.0 (2020-09-29)
------------------

- Added performance improvements to ``get_raw_tissue_reading``.
- Added access to reference data through ``get_raw_reference_reading``.


0.3.0 (2020-09-18)
------------------

- Added backwards compatibility with Mantarray H5 files of v0.1.1.
- Added upload of wheel to PyPI.


0.2.1 (2020-09-04)
------------------

- Removed __version__ as it was causing problems in stand alone applications.
  This will likely be re-added later on.


0.2 (2020-09-02)
------------------

- Added ability to access H5 file directly in WellFile.

