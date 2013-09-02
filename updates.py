#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"
__version__ = "0.1.2.6"

# http://code.activestate.com/recipes/577708-check-for-package-updates-on-pypi-works-best-in-pi/
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

import pip
import sys
import xmlrpclib
from multiprocessing import Pool

class colors:
	""" Colored terminal text
	"""

	HEADER = "\033[95m"
	OKBLUE = "\033[94m"
	OKGREEN = "\033[92m"
	WARNING = "\033[93m"
	FAIL = "\033[91m"
	BOLD = "\033[1m"
	ENDC = "\033[0m"

	def __init__(self):
		pass


def check_package(dist):
	pypi = xmlrpclib.ServerProxy("http://pypi.python.org/pypi")
	available = pypi.package_releases(dist.project_name)
	if not available:
		# try to capitalize pkg name
		available = pypi.package_releases(dist.project_name.capitalize())

	if not available:
		msg = colors.FAIL + u"✖ not found at PyPI" + colors.ENDC
	elif available[0] != dist.version:
		msg = u"{colors.OKGREEN}⤤ {colors.BOLD}{version}{colors.ENDC}".format(colors=colors, version=available[0])
	else:
		if "-v" in sys.argv:
			msg = u"✓ up to date".format(colors=colors)
		else:
			msg = ""
	if msg:
		print(u"{dist.project_name:26} {colors.BOLD}{dist.version:12}{colors.ENDC} {msg}".format(colors=colors, dist=dist, msg=msg))

def main():
	pypi_pool = Pool(42)
	pypi_pool.map(check_package, pip.get_installed_distributions())

if __name__ == "__main__":
	main()