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
import models.rethink.phot.photModel as pm
import models.rethink.user.userModel as um


class InterfaceException(Exception): pass


class BaseInterface(object):
    def __init__(self, model):
        self._model = model

    def _get(self, attr):
        if hasattr(self, attr):
            return object.__getattribute__(self, attr)
        elif attr in self._model:
            return getattr(self._model, attr)
        else:
            raise InterfaceException("Can't find symbol within interface or model!")

    def _set(self, attr, val):
        if attr in self._model and not hasattr(self, attr):
            return object.__setattr__(self._model, attr, val)
        else:
            return object.__setattr__(self, attr, val)

    def __getattr__(self, item):
        return self._get(item)

    def __getitem__(self, item):
        return self._get(item)

    def __setattr__(self, item, value):
        return self._set(item, value)

    def __setitem__(self, item, value):
        return self._set(item, value)

    def __delitem__(self, item):
        pass


class Phot(BaseInterface):
    @property
    def title(self):
        return self._model.title

    @title.setter
    def title(self, title):
        self._model.rename(title)

    @property
    def tags(self):
        return self._model.tags

    @tags.setter
    def tags(self, val):
        tag = [ bit.lstrip().rstrip().lower().replace(" ", "_") for bit in val ]
        self._model.tags = tag
