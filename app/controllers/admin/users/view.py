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
from seshat.objectMods import login, template
from seshat.funcMods import HTML

from seshat.actions import NotFound, Redirect

from errors.general import NotFoundError

from models.rethink.user import userModel as um


@autoRoute()
@login(["admin"])
@template("admin/users/settings", "User")
class view(MixedObject):
    @HTML
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
        email = self.request.getParam("email")
        groups = self.request.getParam("groups")

        if type(groups) is not list:
            groups = [groups]

        groups = [ group.strip(" ").replace(" ", "_").lower() for group in groups if group ]

        user.groups = groups

        if password:
            user.set_password(password)
            self.request.session.push_alert("Password updated, please let the user know the new password", level="warning")

        if email and email != user.email:
          # TODO: Only allow change if email isn't in the database yet
            user.email = email

        user.disable = disable

        user.save()

        return Redirect("/admin/users/"+self.request.id_extended)
