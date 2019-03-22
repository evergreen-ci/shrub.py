#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="shrub.py",
    version="0.2.1",
    description="Library for creating evergreen configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Bradford",
    author_email="david.bradford@mongodb.com",
    url="https://github.com/evergreen-ci/shrub.py",
    license="Apache License, Version 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=[
        "pyyaml",
    ],
)
