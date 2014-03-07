"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
from models.rethink.user import userModel as um

import utils.short_codes as sc


class Invite(BaseInterface):
    table = "invites"

    @classmethod
    def new(cls, email):
        short = sc.generate_short_code(cls.table)

        # TODO: verify email is at least a valid email

        what = cls.create(short_code=short,
                          email=email,
                          created=arrow.utcnow().timestamp,
                          closed=False)

        return what

    @property
    def created(self):
        if not hasattr(self, "_formated_created") or self._formated_created is None:
            self._formated_created = arrow.get(self._data["created"])

        return self._formated_created

    @created.setter
    def created(self, val):
        """
        val should be a unix timestamp of the created datetime instance
        """
        self._formated_created = val
        self._data["created"] = val

    @property
    def user(self):
        if not hasattr(self, "_user") or self._user is None:
            self._user = um.User.from_email(self.email)
        return self._user
