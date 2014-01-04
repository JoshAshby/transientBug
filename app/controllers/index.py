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
            self.view.partial("phot_search", "partials/public/index/phot_search")

            if self.request.session.has_phots:
                self.view.partial("phot_create", "partials/public/index/phot_create")

            if self.request.session.has_screenshots:
                self.view.partial("screenshot", "partials/public/index/screenshot")

            if self.request.session.has_notes:
                self.view.partial("note_create", "partials/public/index/note_create")

            return self.view
        else:
            return Redirect("/phots")
