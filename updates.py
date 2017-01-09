#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mikhail Fedosov (tbs.micle@gmail.com)"
__version__ = "0.1.7.1"

# http://code.activestate.com/recipes/577708-check-for-package-updates-on-pypi-works-best-in-pi/
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

import sys
from packages import Packages
from appearance import Colors, Symbols

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


# packages updated
updated = Packages.create_counter()


def output_package_info(dist, available, status):
    msg = None
    if status == Packages.FAIL:
        msg = u"{colors.fail}{symbols.fail}not found at PyPI{colors.end}".format(colors=Colors, symbols=Symbols)
    elif status == Packages.UPDATED:
        updated.append((dist, available))
        msg = u"{colors.ok}{symbols.update}{colors.bold}{version}{colors.end}".format(colors=Colors, symbols=Symbols, version=available[0])
    else:
        if "-v" in sys.argv:
            msg = u"{symbols.ok}up to date".format(colors=Colors, symbols=Symbols)
    if msg:
        result = u"{dist.project_name:30} {colors.bold}{dist.version:16}{colors.end} {msg}".format(colors=Colors, dist=dist, msg=msg)
        if sys.version_info < (3, 0):
            result = result.encode("utf-8", "replace")
        print(result)


def main():
    packages = Packages(output_package_info)
    packages.check_for_updates()
    if not updated:
        print("Everything up-to-date.")

if __name__ == "__main__":
    main()