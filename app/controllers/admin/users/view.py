#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML

from seshat.actions import NotFound, Redirect

from errors.general import NotFoundError

from models.rethink.user import userModel as um


@route()
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

        self.view.data = {"user": user,
                          "command": self.request.command}

        return self.view

    def POST(self):
        try:
            user = um.User(self.request.id)
        except NotFoundError:
            return NotFound()

        password = self.request.get_param("password")
        disable = self.request.get_param("disable", False)
        email = self.request.get_param("email")
        groups = self.request.get_param("groups")
        clear_reset = self.request.get_param("clear_reset", False)

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

        if clear_reset:
            del user.reset_code

        user.disable = disable

        user.save()

        return Redirect("/admin/users/"+self.request.id_extended)
