#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.MixedObject import MixedObject
from seshat.objectMods import login

from seshat.actions import NotFound, Redirect

from errors.general import NotFoundError

from models.rethink.user import userModel as um


@login(["admin"])
@autoRoute()
class view(MixedObject):
    _title = "Users"
    _default_tmpl = "admin/users/settings"
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "users"})
        try:
            user = um.User(self.request.id)

        except NotFoundError:
            return NotFound()

        self.view.title = user.username


        self.view.partial("tabs",
                          "partials/admin/users/tabs",
                          {"user": user,
                           "command": self.request.command})

        self.view.data = {"user": user}

        return self.view

    def POST(self):
        try:
            user = um.User(self.request.id)
        except NotFoundError:
            return NotFound()

        password = self.request.getParam("password")
        disable = self.request.getParam("disable", False)

        if password:
            user.set_password(password)

        user.disable = disable

        user.save()

        return Redirect("/admin/users/"+self.request.id_extended)
