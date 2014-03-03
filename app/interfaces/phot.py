#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from interfaces.base_interface import BaseInterface
import models.rethink.user.userModel as um


class Phot(BaseInterface):
    _user = None

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

    @property
    def user(self):
        if self._user is None:
            self._user = um.User(self._model.user)
        return self._user

    @user.setter
    def user(self, val):
        if isinstance(val, um.User):
            self._model.user = val.id
        else:
            self._model.user = val

        self._user = um.User(self._model.user)
