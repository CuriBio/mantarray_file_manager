# -*- coding: utf-8 -*-
"""Setup configuration."""
from setuptools import find_packages
from setuptools import setup


setup(
    name="mantarray_file_manager",
    version="0.5.0",
    description="Finds and opens Mantarray files.",
    url="https://github.com/CuriBio/mantarray-file-manager",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "h5py>=2.10.0",
        "nptyping>=1.3.0",
        "numpy>=1.20.2",
        "stdlib-utils>=0.2.1",
        "semver>=2.10.2",
        "immutable_data_validation>=0.2.1",
        "immutabledict>=1.1.0",
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
)
