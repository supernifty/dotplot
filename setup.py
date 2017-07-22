#!/usr/bin/env python

import setuptools
import pathlib

name = "dotplot"
version = "0.1"
release = "0.1.0"
here = pathlib.Path(__file__).parent.resolve()

setuptools.setup(
    name=name,
    version=version,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'dotplot = dotplot.main:main',
        ],
    },
    install_requires=[
        'Pillow',
    ],
    license="LICENSE"
)
