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
from seshat.objectMods import template, login
from seshat.funcMods import HTML


@autoRoute()
@login(redirect="/phots", quiet=True)
@template("public/index/index", "Home")
class index(MixedObject):
    @HTML
    def GET(self):
        if self.request.session.id:
            self.view.partial("sidebar", "partials/public/index/sidebar",
                             {"req": self.request})
            return self.view
        else:
            return Redirect("/phots")
