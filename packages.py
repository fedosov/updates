# -*- coding: utf-8 -*-
import pip
import sys
import socket
if sys.version_info < (3, 0):
    from xmlrpclib import ServerProxy
else:
    from xmlrpc.client import ServerProxy
from multiprocessing import Pool
from itertools import izip_longest


def check_package(args):
    dist, status_callback = args
    callback = lambda status: status_callback(dist, available, status)
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
            callback(Packages.FAIL)
        elif available[0] != dist.version:
            callback(Packages.UPDATED)
        else:
            callback(Packages.OK)

    except socket.timeout:
        callback(Packages.FAIL)

    except KeyboardInterrupt:
        return False


class Packages(object):
    OK = 1
    FAIL = 2
    UPDATED = 4

    def __init__(self, callback):
        self.updated = 0
        self.status_callback = callback

    def check_for_updates(self):
        self.updated = 0
        socket.setdefaulttimeout(5.0)
        dists = pip.get_installed_distributions()
        if sys.platform == "win32":
            map(check_package, dists)
        else:
            pypi_pool = Pool()
            pypi_pool_map = pypi_pool.map_async(check_package, izip_longest(dists, [], fillvalue=self.status_callback))
            try:
                pypi_pool_map.get(0xFFFF)
            except KeyboardInterrupt:
                print("Aborted")
