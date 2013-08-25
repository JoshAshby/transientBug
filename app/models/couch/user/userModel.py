#!/usr/bin/env python
"""
fla.gr user model

Given a userID or a username or a email, return the users couchc.database ORM

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""

from couchdb.mapping import Document, TextField, DateTimeField, \
        BooleanField, IntegerField, ViewField
import bcrypt
from datetime import datetime

import config.config as c
import utils.markdownUtils as mdu

from models.modelExceptions.userModelExceptions import \
       multipleUsersError, passwordError, userError

from models.couch.baseCouchModel import baseCouchModel


class User(Document, baseCouchModel):
    """
    Base ORM for users in fla.gr, this one currently uses couchc.database to store
    the data.
    TODO: Flesh this doc out a lot more
    """
    _name = "users"
    username = TextField()
    email = TextField()
    about = TextField(default="")
    disable = BooleanField(default=False)
    level = IntegerField(default=1)
    password = TextField()
    created = DateTimeField(default=datetime.now)
    docType = TextField(default="user")
    formated_created = ""
    formated_about = ""

    _view = "stuff/users"

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
            user = cls(username=username, password=passwd)
            return user
        else:
            raise userError("That username is taken, please choose again.",
                    username)

    def set_password(self, password):
        """
        Sets the users password to `password`

        :param password: plain text password to hash
        """
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.store(c.database.couchServer)

    @staticmethod
    def _search(items, value):
        """
        Searches the list `items` for the given value

        :param items: A list of ORM objects to search
        :param value: The value to search for, in this case
            value can be a username or an email, or an id
        """
        foundUser = []
        for user in items:
            if user.email == value \
                    or user.username == value \
                    or user.id == value:
                foundUser.append(user)
        if not foundUser:
            return None
        if len(foundUser)>1:
            raise multipleUsersError("Multiple Users", value)
        else:
            user = foundUser[0]
            user.format()
            return user

    @property
    def has_admin(self):
        return self.level > 50

    def format(self):
        """
        Formats markdown and dates into the right stuff
        """
        self.formated_about = mdu.markClean(self.about)
        self.formated_created = datetime.strftime(self.created, "%a %b %d, %Y @ %H:%I%p")

    #@classmethod
    #def find(cls, what):
      #for bit in cls._view(c.general.couch): print bit

      #results = list(c.general.couch.query(cls._view.map_fun, key=what).rows)

      #if len(results) > 0:
          #print results[0].value
          #return results[0].doc
      #return None
