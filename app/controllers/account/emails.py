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
class emails(MixedObject):
    _title = "Account Settings - Emails"
    _default_tmpl = "public/account/index"
    def GET(self):
        user = um.User(self.request.session.id)

        self.view.partial("tabs",
                          "partials/public/account/tabs",
                          {"user": user,
                           "command": "emails"})

        self.view.data = {"user": user}
        return self.view