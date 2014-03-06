#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"
__version__ = "0.1.5"

# http://code.activestate.com/recipes/577708-check-for-package-updates-on-pypi-works-best-in-pi/
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

import pip
import sys
import socket
from multiprocessing import Pool
from appearance import Colors, Symbols

if sys.version_info < (3, 0):
    from xmlrpclib import ServerProxy
else:
    from xmlrpc.client import ServerProxy

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding("utf-8")
else:
    # http://stackoverflow.com/questions/3828723/why-we-need-sys-setdefaultencodingutf-8-in-a-py-script
    pass

# disable colors and simplify status symbols for Windows console
if sys.platform == "win32":
    Colors.disable()
    Symbols.simplify()


def check_package(dist):
    pypi = ServerProxy("http://pypi.python.org/pypi")

    try:
        available = pypi.package_releases(dist.project_name)
        if not available:
            # try to capitalize pkg name
            available = pypi.package_releases(dist.project_name.capitalize())
            if not available:
                # try to replace "-" by "_" (as in "django_compressor")
                available = pypi.package_releases(dist.project_name.replace("-", "_"))

        if not available:
            msg = u"{colors.fail}{symbols.fail}not found at PyPI{colors.end}".format(colors=Colors, symbols=Symbols)
        elif available[0] != dist.version:
            msg = u"{colors.ok}{symbols.update}{colors.bold}{version}{colors.end}".format(colors=Colors, symbols=Symbols, version=available[0])
        else:
            if "-v" in sys.argv:
                msg = u"{symbols.ok}up to date".format(colors=Colors, symbols=Symbols)
            else:
                msg = ""
    except socket.timeout:
        msg = u"{colors.fail}{symbols.fail}timeout{colors.end}".format(colors=Colors, symbols=Symbols)
    except KeyboardInterrupt:
        return False

    if msg:
        print((u"{dist.project_name:26} {colors.bold}{dist.version:16}{colors.end} {msg}".format(colors=Colors, dist=dist, msg=msg)).encode("utf-8", "replace"))


def main():
    socket.setdefaulttimeout(5.0)
    # do not use multiprocessing under Windows
    if sys.platform == "win32":
        map(check_package, pip.get_installed_distributions())
    else:
        pypi_pool = Pool()
        pypi_pool_map = pypi_pool.map_async(check_package, pip.get_installed_distributions())
        try:
            pypi_pool_map.get(0xFFFF)
        except KeyboardInterrupt:
            print("Aborted")
            return

if __name__ == "__main__":
    main()