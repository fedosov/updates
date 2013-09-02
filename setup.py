# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"

import os
import re
from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))

def get_version():
	f = open(os.path.join(here, "updates.py"))
	version_file = f.read()
	f.close()
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
	                          version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")

setup_params = \
{
	"entry_points":
	{
		"console_scripts":
		[
			"updates=updates:main",
		]
	}
}

setup(
	name="updates",
    version=get_version(),
    description="Check for updated packages in the PyPI",
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
	py_modules=["updates"],
    **setup_params
)