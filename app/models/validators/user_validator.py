#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.rethink.user.userModel as um


class UserValidator(object):
    _user_field = ""
    _user_cache = None

    @property
    def author(self):
        return self.user

    @author.setter
    def author(self, val):
        self.user = val

    @property
    def user(self):
        if not hasattr(self, "_user_cache") or self._user_cache is None:
            self._user_cache = um.User(self._data.get(self._user_field))
        return self._user_cache

    @user.setter
    def user(self, val):
        if isinstance(val, um.User):
            self._data[self._user_field] = val.id
        else:
            self._data[self._user_field] = val

        self._user_cache = um.User(self._data[self._user_field])
