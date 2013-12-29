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
from seshat.actions import Redirect
from seshat.objectMods import login

import rethinkdb as r
from models.rethink.user import userModel as um


@login()
@autoRoute()
class index(MixedObject):
    _title = "Account Settings"
    _default_tmpl = "public/account/index"
    def GET(self):
        user = um.User(self.request.session.id)

        self.view.partial("tabs",
                          "partials/public/account/tabs",
                          {"user": user,
                           "command": self.request.command})

        self.view.data = {"user": user}
        return self.view

    def POST(self):
        error = False
        user = um.User(self.request.session.id)

        email = self.request.getParam("email")
        password = self.request.getParam("password")

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
