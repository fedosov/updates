# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"

import os
import re
from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))


def get_version():
    with open(os.path.join(here, "updates.py")) as upy:
        version_file = upy.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup_params = {
    "entry_points": {
        "console_scripts": [
            "updates=updates:main",
        ]
    }
}

## Get long_description from index.txt:
f = open(os.path.join(here, "docs", "index.rst"))
long_description = f.read().strip()
f.close()

setup(
    name="updates",
    version=get_version(),
    description="Check for updated packages in the PyPI",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="pip updates update pypi packages",
    author="Mikhail Fedosov",
    author_email="tbs.micle@gmail.com",
    url="https://github.com/fedosov/updates",
    license="MIT",
    py_modules=["appearance", "packages", "updates"],
    **setup_params
)