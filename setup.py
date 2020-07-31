# -*- coding: utf-8 -*-
"""Setup configuration."""
from setuptools import find_packages
from setuptools import setup


setup(
    name="mantarray_file_manager",
    version="0.1",
    description="CREATE A DESCRIPTION",
    url="https://github.com/CuriBio/mantarray_file_manager",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
)
