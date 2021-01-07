Changelog for Mantarray File Manager
====================================


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

