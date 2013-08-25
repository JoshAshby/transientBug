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

import models.couch.user.userModel as um


class session(brm.redisObject):
    def _finishInit(self):
        if not hasattr(self, "rawAlerts"): self.rawAlerts = "[]"
        if not hasattr(self, "username"): self.username = None
        if not hasattr(self, "userID"): self.userID = None
        if not hasattr(self, "has_admin"): self.has_admin = None

    def loginWithoutCheck(self, user):
        """
        Tries to find the user in the database, if the user is successfully
        logged in then the sessions username and user ID is set to that users

        :param user: Str of the username or ID to try and login
        :type user: Str

        :returns: True if the user was successfully logged in
        """
        foundUser = um.User.find(user)
        if foundUser:
            if not foundUser.disable:
                self.username = foundUser.username
                self.userID = foundUser.id
                self.has_admin = foundUser.has_admin
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
        foundUser = um.User.find(user)
        if foundUser:
            if not foundUser.disable:
                if foundUser.password == bcrypt.hashpw(password,
                        foundUser.password):
                    self.username = foundUser.username
                    self.userID = foundUser.id
                    self.has_admin = foundUser.has_admin
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
        self.username = None
        self.userID = None
        self.has_admin = None
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
