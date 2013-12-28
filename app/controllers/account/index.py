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


@login()
@autoRoute()
class index(MixedObject):
    _title = "Account Settings"
    _default_tmpl = "public/account/index"
    def GET(self):
        return self.view

    def POST(self):
        email = self.request.getParam("email")
        password = self.request.getParam("password")
