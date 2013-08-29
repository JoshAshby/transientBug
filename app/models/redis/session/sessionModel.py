#!/usr/bin/env python
"""
fla.gr session model

Takes advantage of collections to make a dynamic system allowing
both regular needed session data along with temporary session data storage
available to the system through the requests object

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import bcrypt
import models.redis.baseRedisModel as brm
import models.modelExceptions.sessionExceptions as use
import json

import models.rethink.user.userModel as um
import rethinkdb as r


class session(brm.redisObject):
    groups = []
    def _finishInit(self):
        if not hasattr(self, "rawAlerts"): self.rawAlerts = "[]"
        if not hasattr(self, "username"): self.username = ""
        if not hasattr(self, "userID"): self.userID = ""
        if not hasattr(self, "groups"): self.groups = []

    def _get(self, item):
        if "groups" in self._keys:
            groups = self._keys["groups"]
            if "has_" in item:
                if "root" in groups or (item[4:] in groups):
                    return True
                else:
                    return False
        if item not in object.__getattribute__(self, "protectedItems") \
                and item[0] != "_":
            keys = object.__getattribute__(self, "_keys")
            if item in keys:
                return keys[item]
        return object.__getattribute__(self, item)

    def loginWithoutCheck(self, user):
        """
        Tries to find the user in the database, if the user is successfully
        logged in then the sessions username and user ID is set to that users

        :param user: Str of the username or ID to try and login
        :type user: Str

        :returns: True if the user was successfully logged in
        """
        foundUser = list(r.table(um.User.table).filter({'username': user}).run())
        if len(foundUser) > 0:
            foundUser = um.User(foundUser[0]["id"])
            if not foundUser.disable:
                self.username = foundUser.username
                self.userID = foundUser.id
                self.groups = foundUser.groups
                return True
            else:
                raise use.banError("Your user is currently disabled. \
                        Please contact an admin for additional information.")
        raise use.usernameError("We can't find your user, are you \
                sure you have the correct information?")

    def login(self, user, password):
        """
        Tries to find the user in the database,then tries to use the plain text
        password from `password` to match against the known password hash in
        the users object. If the user is successfully logged in then the sessions
        username and user ID is set to that users

        :param user: Str of the username or ID to try and login
        :type user: Str
        :param password: Clear text str of the users password to hash and check
        :type password: Str

        :returns: True if the user was successfully logged in
        """
        foundUser = list(r.table(um.User.table).filter({'username': user}).run())
        if len(foundUser) > 0:
            foundUser = um.User.fromRawEntry(**foundUser[0])
            if not foundUser.disable:
                if foundUser.password == bcrypt.hashpw(password,
                        foundUser.password):
                    self.username = foundUser.username
                    self.userID = foundUser.id
                    self.groups = foundUser.groups
                    return True
                else:
                    raise use.passwordError("Your password appears to \
                            be wrong.")
            else:
                raise use.banError("Your user is currently disabled. \
                        Please contact an admin for additional information.")
        raise use.usernameError("We can't find your user, are you \
                sure you have the correct information?")

    def logout(self):
        """
        Sets the users loggedIn to False then removes the link between their
        session and their `userORM`
        """
        self.username = ""
        self.userID = ""
        self.groups = []
        return True

    def pushAlert(self, message, quip="", level="success"):
        """
        Creates an alert message to be displayed or relayed to the user,
        This is a higher level one for use in HTML templates.
        All params are of type str

        :param message: The text to be placed into the main body of the alert
        :param quip: Similar to a title, however just a quick attention getter
        :param level: Can be any of `success` `error` `info` `warning`
        """
        alerts = json.loads(self.rawAlerts)
        alerts.append({"msg": message, "level": level, "expire": "next", "quip": quip})
        self.rawAlerts = json.dumps(alerts)

    @property
    def alerts(self):
        """
        Returns a list of dictonary elements representing the users alerts

        :return: List of Dicts
        """
        return json.loads(self.rawAlerts)

    @alerts.deleter
    def alerts(self):
        """
        Clears the current users expired alerts.
        """
        alerts = json.loads(self.rawAlerts)
        for alert in alerts:
            if alert["expire"] == "next":
                alerts.pop(alerts.index(alert))

        self.rawAlerts = json.dumps(alerts)

    def renderAlerts(self):
        alerts = json.loads(self.rawAlerts)

        alertStr = ""
        for alert in alerts:
            if alert["level"] == "info":
                alert["icon"] = "info-sign"
            elif alert["level"] == "success":
                alert["icon"] = "thumbs-up"
            elif alert["level"] == "warning":
                alert["icon"] = "excalmation-mark"
            elif alert["level"] == "error":
                alert["icon"] = "warning-sign"

            alertStr += ("""<div class="alert alert-{level}"><i class="icon-{icon}"></i><strong>{quip}</strong> {msg}</div>""").format(**alert)

        self._HTMLAlerts = unicode(alertStr)

    def has_perm(self, group_name):
        if group_name in self.groups:
            return True
        return False
