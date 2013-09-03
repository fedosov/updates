#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"
__version__ = "0.1.3.4"

# http://code.activestate.com/recipes/577708-check-for-package-updates-on-pypi-works-best-in-pi/
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

import pip
import sys
import socket
import xmlrpclib
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding("utf-8")

class colors:
	""" Colored terminal text
	"""
	OKGREEN = "\033[92m"
	FAIL = "\033[91m"
	BOLD = "\033[1m"
	ENDC = "\033[0m"

	@classmethod
	def disable(cls):
		colors.OKGREEN = ""
		colors.FAIL = ""
		colors.BOLD = ""
		colors.ENDC = ""


class symbols:
	""" Status symbols
	"""
	FAIL = u"✖ "
	UPDATE = u"⤤ "
	OK = u"✓ "

	@classmethod
	def disable(cls):
		symbols.FAIL = ""
		symbols.UPDATE = ""
		symbols.OK = ""

	@classmethod
	def simplify(cls):
		symbols.FAIL = "x "
		symbols.UPDATE = "+ "
		symbols.OK = ""


# disable colors and simplify status symbols for Windows console
if sys.platform == "win32":
	colors.disable()
	symbols.simplify()

def check_package(dist):
	pypi = xmlrpclib.ServerProxy("http://pypi.python.org/pypi")

	try:
		available = pypi.package_releases(dist.project_name)
		if not available:
			# try to capitalize pkg name
			available = pypi.package_releases(dist.project_name.capitalize())

		if not available:
			msg = u"{colors.FAIL}{symbols.FAIL}not found at PyPI{colors.ENDC}".format(colors=colors, symbols=symbols)
		elif available[0] != dist.version:
			msg = u"{colors.OKGREEN}{symbols.UPDATE}{colors.BOLD}{version}{colors.ENDC}".format(colors=colors, symbols=symbols, version=available[0])
		else:
			if "-v" in sys.argv:
				msg = u"{symbols.OK}up to date".format(colors=colors, symbols=symbols)
			else:
				msg = ""
	except socket.timeout:
		msg = u"{colors.FAIL}{symbols.FAIL}timeout{colors.ENDC}".format(colors=colors, symbols=symbols)

	if msg:
		print((u"{dist.project_name:26} {colors.BOLD}{dist.version:16}{colors.ENDC} {msg}".format(colors=colors, dist=dist, msg=msg)).encode("utf-8", "replace"))

def main():
	socket.setdefaulttimeout(5.0)
	# do not use multiprocessing under Windows
	if sys.platform == "win32":
		map(check_package, pip.get_installed_distributions())
	else:
		pypi_pool = Pool()
		pypi_pool.map(check_package, pip.get_installed_distributions())

if __name__ == "__main__":
	main()