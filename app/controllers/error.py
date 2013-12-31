#!/usr/bin/env python
"""
main error pages

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.objectMods import template
from seshat.funcMods import HTML
from seshat.MixedObject import MixedObject


@template("error/404", "404 NOT FOUND")
class error404(MixedObject):
    @HTML
    def GET(self):
        self.head = ("404 NOT FOUND", [("Content-Type", "text/html")])
        return self.view


@template("error/401", "401 UNAUTHORIZED")
class error401(MixedObject):
    @HTML
    def GET(self):
        self.head = ("401 UNAUTHORIZED", [("Content-Type", "text/html")])
        return self.view


@template("error/500", "500 INTERNAL SERVER ERROR")
class error500(MixedObject):
    @HTML
    def GET(self):
        self.head = ("500 INTERNAL SERVER ERROR", [("Content-Type", "text/html")])
        self.view.data = {"error": self.request.error[0], "tb": self.request.error[1]}
        return self.view
