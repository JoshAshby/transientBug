#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow


class CreatedValidator(object):
    _created_field = ""
    _created_cache = None

    @property
    def created(self):
        if not hasattr(self, "_created_cache") or self._created_cache is None:
            self._created_cache = arrow.get(self._data[self._created_field])

        return self._created_cache

    @created.setter
    def created(self, val):
        """
        val should be a unix timestamp of the created datetime instance
        """
        self._created_cache = None
        self._data[self._created_field] = val
