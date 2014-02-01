#!/usr/bin/env python
"""
main error pages

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML
from seshat_addons.seshat.mixed_object import MixedObject

from seshat.head import Head


@template("error/404", "404 NOT FOUND")
class error404(MixedObject):
    @HTML
    def GET(self):
        self.head = Head("404 NOT FOUND", [("Content-Type", "text/html")])
        return self.view


@template("error/401", "401 UNAUTHORIZED")
class error401(MixedObject):
    @HTML
    def GET(self):
        self.head = Head("401 UNAUTHORIZED", [("Content-Type", "text/html")])
        return self.view


@template("error/500", "500 INTERNAL SERVER ERROR")
class error500(MixedObject):
    @HTML
    def GET(self):
        self.head = Head("500 INTERNAL SERVER ERROR", [("Content-Type", "text/html")])
        self.view.data = {"error": self._error[0], "tb": self._error[1]}
        return self.view
