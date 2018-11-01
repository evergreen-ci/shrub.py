#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages


setup(
    name='shrub.py',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'pyyaml',
    ],
)
