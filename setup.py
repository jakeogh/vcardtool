# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

if not sys.version_info[0] == 3:
    sys.exit("Python 3 is required. Use: \'python3 setup.py install\'")

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "vcardtool",
    "url": "https://github.com/jakeogh/vcardtool",
    "license": "PUBLIC DOMAIN",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "Split a multiple record vcard .vcf file into individual .vcf files",
    "long_description": __doc__,
    "packages": find_packages(exclude=['tests']),
    "package_data": {"vcardtool": ['py.typed']},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "vcardtool=vcardtool.vcardtool:cli",
        ],
    },
}

setup(**config)
