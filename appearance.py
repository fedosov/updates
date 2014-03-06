# -*- coding: utf-8 -*-


class Colors(object):
    """ Colored terminal text
    """
    ok = "\033[92m"
    fail = "\033[91m"
    bold = "\033[1m"
    end = "\033[0m"

    @classmethod
    def disable(cls):
        cls.ok = ""
        cls.fail = ""
        cls.bold = ""
        cls.end = ""


class Symbols(object):
    """ Status symbols
    """
    fail = u"✖ "
    update = u"+ "
    ok = u"✓ "

    @classmethod
    def disable(cls):
        cls.fail = ""
        cls.update = ""
        cls.ok = ""

    @classmethod
    def simplify(cls):
        cls.fail = "x "
        cls.update = "+ "
        cls.ok = ""
