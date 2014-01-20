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
from seshat_addons.MixedObject import MixedObject
from seshat.actions import Redirect
from seshat_addons.objectMods import login, template
from seshat_addons.funcMods import HTML

import rethinkdb as r
from models.rethink.user import userModel as um


@route()
@login()
@template("public/account/index", "Account Settings")
class index(MixedObject):
    @HTML
    def GET(self):
        user = um.User(self.request.session.id)

        self.view.partial("tabs",
                          "partials/public/account/tabs",
                          {"user": user,
                           "command": self.request.command})

        self.view.data = {"user": user}
        return self.view

    @HTML
    def POST(self):
        error = False
        user = um.User(self.request.session.id)

        email = self.request.get_param("email")
        password = self.request.get_param("password")

        if email and email != user.email:
            found = r.table(um.User.table).filter({"email": email})\
                .map(lambda u: u["id"]).coerce_to("array").run()

            if email in found:
                error = True
                self.view.data = {
                    "error": "email",
                    "msg": "That email is already registered, please choose another."
                    }
            else:
                user.email = email

        if password:
            user.set_password(password)
            self.request.session.push_alert("Password updated, please make sure to use it :)", level="warning")

        user.save()

        if error:
            return self.view

        return Redirect("/account")
