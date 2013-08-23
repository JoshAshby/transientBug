"""
User model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkModel
import arrow
import bcrypt

import utils.markdownUtils as mdu

from models.modelExceptions.userModelExceptions import \
       passwordError, userError


class User(RethinkModel):
    table = "users"
    _protectedItems = ["formatedAbout", "formatedCreated", "hasAdmin"]
    @classmethod
    def new_user(cls, username, password):
        """
        Make a new user, checking for username conflicts. If no conflicts are
        found the password is encrypted with bcrypt and the resulting `userORM` returned.

        :param username: The username that should be used for the new user
        :param password: The plain text password that should be used for the password.
        :return: `userORM` if the username is available,
        """
        if password == "":
            raise passwordError("Password cannot be null")
        elif not cls.find(username):
            passwd = bcrypt.hashpw(password, bcrypt.gensalt())
            user = cls(username=username,
                       password=passwd,
                       created=arrow.utcnow().timestamp,
                       disabled=False,
                       alerts="")
            return user
        else:
            raise userError("That username is taken, please choose again.",
                    username)

    def setPassword(self, password):
        """
        Sets the users password to `password`

        :param password: plain text password to hash
        """
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.save()

    @property
    def hasAdmin(self):
        return self.level > 50

    def format(self):
        """
        Formats markdown and dates into the right stuff
        """
        self.formatedAbout = mdu.markClean(self.about)
        self.formatedCreated = arrow.get(self.created)
