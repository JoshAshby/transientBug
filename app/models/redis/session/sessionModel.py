#!/usr/bin/env python
"""
Seshat

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import json
import uuid
import bcrypt
import rethinkdb as r
from cookies import Cookie

from redisORM import RedisModel

from seshat.session import Session as BaseSession

import errors.session as use
import models.rethink.user.userModel as um


class Session(BaseSession):
    cookie_id = "bug_sid"
    _user_cache = None

    def load(self):
        namespace = "session"
        if self.request.headers.authorization is None:
            if not self.cookie_id in self.request.headers.cookies:
                self.request.headers.cookies.add(Cookie(self.cookie_id, str(uuid.uuid4())))

            key = self.request.headers.cookies[self.cookie_id].value

        elif self.request.headers.authorization:
            key = self.request.headers.authorization.username

        self.data = RedisModel(namespace, key)
        self.key = key

        if self.request.headers.authorization:
            try:
                self.login(self.request.headers.authorization.username, self.request.headers.authorization.password)
            except:
                self.logout()

        if not "alerts" in self.data:
            self.data["alerts"] = []

        if not "groups" in self.data:
            self.data["groups"] = []

    def save(self, response):
        if int(response.status[:3]) not in [303]:
            del self.alerts

      # TODO: Rotate the session key each time? This should help preventing old
      # sessions from being used

      # TODO: Set a key expire for each redis key. This is a feature that needs
      # to be added to RedisORM anyways so I'll wait till thats a go before
      # adding it here.

        for cookie in self.request.headers.cookies.all_cookies:
            val = cookie.render_response()
            response.headers.append("Set-Cookie", val)

    @property
    def alerts(self):
        return self.data["alerts"]

    def _render_alerts(self):
        alerts = [ json.loads(s) for s in self.alerts ]
      # TODO: Move this out of the session and into templates.
        alertStr = ""
        for alert in alerts:
            if alert["level"] in ["info"]:
                alert["icon"] = "info"
            elif alert["level"] in ["success"]:
                alert["icon"] = "thumbs-up"
            elif alert["level"] in ["warning"]:
                alert["icon"] = "excalmation"
            elif alert["level"] in ["danger", "error"]:
                alert["icon"] = "warning"
                alert["level"] = "danger"

            alertStr += ("""<div class="alert alert-{level}"><i class="fa fa-{icon}"></i> <strong>{quip}</strong> {msg}</div>""").format(**alert)

        return unicode(alertStr)

    @alerts.deleter
    def alerts(self):
        """
        Clears the current users expired alerts.
        """
        for alert in self.alerts:
            raw = alert
            alert = json.loads(alert)
            if alert["expire"] == "next":
                self.alerts.remove(raw)

    @alerts.setter
    def alerts(self, val):
        assert isinstance(val, dict)
        base = {"msg": "", "level": "success", "expire": "next", "quip": ""}
        base.update(val)
        self.alerts.append(json.dumps(base))

    def push_alert(self, message, quip="", level="success", expires=None):
        """
        Creates an alert message to be displayed or relayed to the user,
        This is a higher level one for use in HTML templates.
        All params are of type str

        :param message: The text to be placed into the main body of the alert
        :param quip: Similar to a title, however just a quick attention getter
        :param level: Can be any of `success` `error` `info` `warning`
        """
        expires = expires or "next"
        alert = {"msg": message, "level": level, "expire": expires, "quip": quip}
        self.alerts.append(json.dumps(alert))

    @property
    def user(self):
        if not hasattr(self, "_user_cache") or self._user_cache is None:
            if "user" in self.data:
                self._user_cache = um.User(self.data.get("user"))
                if not self._user_cache.id:
                    self._user_cache = None
            else:
                self._user_cache = None
        return self._user_cache

    @user.setter
    def user(self, val):
        if isinstance(val, um.User):
            self.data["user"] = val.id
        else:
            self.data["user"] = val

        self._user_cache = um.User(self.data["user"]) if self.data["user"] else None
        self.data["groups"] = self._user_cache["groups"]

    @property
    def id(self):
        return self.data["user"] if "user" in self.data else None

    @property
    def groups(self):
        return self.data["groups"]

    def has_perm(self, group_name):
        return self.has_group(group_name)

    def has_group(self, group_name):
        if group_name in self.data.groups or "root" in self.data.groups:
            return True

        return False

    def login(self, user, password):
        """
        Tries to find the user in the database,then tries to use the plain text
        password from `password` to match against the known password hash in
        the users object. If the user is successfully logged in then the
        sessions `user` entry is set to that of the users id

        :param user: Str of the username or ID to try and login
        :type user: Str
        :param password: Clear text str of the users password to hash and check
        :type password: Str

        :returns: True if the user was successfully logged in

        :raises SessionError: Will raise a subclass of
            :py:class:`.SessionError` if there was a problem logging the user in
        """
        reg = "(?i)^{}$".format(user)
        foundUser = r.table(um.User.table)\
                .filter(lambda doc: doc["username"].match(reg))\
                .coerce_to("array")\
                .run()

        if foundUser:
            foundUser = um.User(**foundUser[0])
            if not foundUser.disable:
                if str(foundUser.password) == bcrypt.hashpw(str(password), str(foundUser.password)):
                    self.user = foundUser
                    return True

                else:
                    raise use.PasswordError("Your password appears to \
                            be wrong.")

            else:
                raise use.DisableError("Your user is currently disabled. \
                        Please contact an admin for additional information.")

        raise use.UsernameError("We can't find your user, are you \
                sure you have the correct information?")

    def logout(self):
        del self.data["groups"]
        del self.data["user"]
        self._user_cache = None
        return True
