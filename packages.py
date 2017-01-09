# -*- coding: utf-8 -*-
import pip
import sys
import socket
import multiprocessing
if sys.version_info < (3, 0):
    from xmlrpclib import ServerProxy
    from itertools import izip_longest as zip_longest
else:
    from xmlrpc.client import ServerProxy
    from itertools import zip_longest
    from functools import reduce


def check_package(args):
    dist, status_callback = args
    pypi = ServerProxy("https://pypi.python.org/pypi")
    available = None
    callback = lambda status: status_callback(dist, available, status)
    try:
        possible_package_names = [dist.project_name,
                                  dist.project_name.capitalize(),
                                  dist.project_name.replace("-", "_")]
        available = reduce(lambda a, b: a if a is not None else b, map(pypi.package_releases, possible_package_names))
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

    @classmethod
    def use_multiprocessing(cls):
        return sys.platform != "win32"

    @classmethod
    def create_counter(cls):
        if cls.use_multiprocessing():
            return multiprocessing.Manager().list()
        else:
            return list()

    def check_for_updates(self):
        self.updated = 0
        socket.setdefaulttimeout(5.0)
        dists = pip.get_installed_distributions()
        map_params = (check_package, zip_longest(dists, [], fillvalue=self.status_callback))
        if self.use_multiprocessing():
            pypi_pool = multiprocessing.Pool()
            pypi_pool_map = pypi_pool.map_async(*map_params)
            try:
                pypi_pool_map.get(0xFFFF)
            except KeyboardInterrupt:
                print("Aborted")
        else:
            map(*map_params)
