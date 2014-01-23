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
from seshat.actions import Redirect
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import template, login
from seshat_addons.func_mods import HTML


@route()
@login(redirect="/phots", quiet=True)
@template("public/index/index", "Home")
class index(MixedObject):
    @HTML
    def GET(self):
        if self.request.session.id:
            self.view.partial("sidebar", "partials/public/index/sidebar",
                             {"req": self.request})
            self.view.partial("phot_search", "partials/public/phot_search")

            if self.request.session.has_phots:
                self.view.partial("phot_create", "partials/public/phot_create")

            if self.request.session.has_screenshots:
                self.view.partial("screenshot",
                    "partials/public/screenshot_create")

            if self.request.session.has_notes:
                self.view.partial("note_create", "partials/public/note_create")

            return self.view
        else:
            return Redirect("/phots")
