#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkModel

class InterfaceException(Exception): pass


class BaseInterface(RethinkModel):
    def _get(self, attr):
        pro_its = object.__getattribute__(self, "_protected_items")
        if attr[0] == "_" or attr in pro_its:
            return object.__getattribute__(self, attr)

        else:
            data = object.__getattribute__(self, "_data")
            if hasattr(self, attr):
                return object.__getattribute__(self, attr)

            else:
                return data[attr]


    def _set(self, attr, val):
        pro_its = object.__getattribute__(self, "_protected_items")
        if attr[0] == "_" or attr in pro_its:
            return object.__setattr__(self, attr, val)

        else:
            data = object.__getattribute__(self, "_data")
            if hasattr(val, "__call__") or hasattr(self, attr):
                return object.__setattr__(self, attr, val)

            else:
                data[attr] = val
                return val
