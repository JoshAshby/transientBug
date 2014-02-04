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
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template, login
from seshat_addons.seshat.func_mods import HTML


@route()
@login(redirect="/phots", quiet=True)
@template("public/index/index", "Home")
class index(MixedObject):
    @HTML
    def GET(self):
        if self.request.session.id:
            return self.view

        else:
            return Redirect("/phots")
