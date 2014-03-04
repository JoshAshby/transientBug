#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r
from rethinkORM import RethinkModel


class InterfaceException(Exception): pass


class BaseInterface(RethinkModel):
    def __init__(self, id=None, **kwargs):
        """
        Initializes the main object, if `id` is the only thing passed then we
        assume this document is already in the database and grab its data,
        otherwise we treat it as a new object.

        (Optional, only if not using .repl()) `conn` or `connection` can also
        be passed, which will be used in all the .run() clauses.
        """

        # Is this a new object, or already in the database? (set later)
        self._data = {}  # STORE ALL THE DATA!!

        # If we're given a connection, we'll use it, if not, we'll assume
        # .repl() was called on r.connect()
        if "conn" in kwargs:
            self._conn = kwargs.pop("conn")
        elif "connection" in kwargs:
            self._conn = kwargs.pop("connection")

        key = kwargs[self._primary_key] if self.primary_key in kwargs else id

        if len(kwargs) == 0 and key:
          rawCursor = r.table(self.table).get(key).run(self._conn)
          if rawCursor:
              self._data = dict(rawCursor)
          else:
              raise Exception("No document found for id: "+str(key))

        else:
            for item in kwargs:
                if item not in self._protected_items and item[0] != "_":
                    self._data[item] = kwargs[item]
            self._data[self.primary_key] = key

        # Hook to run any inherited class code, if needed
        self.finish_init()

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

    def __json__(self):
        return dict()
