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

from seshat.response import Response


@template("error/404", "404 NOT FOUND")
class error404(MixedObject):
    @HTML
    def GET(self):
        return Response(404, [("Content-Type", "text/html")], self.view.render())

    def POST(self):
        return self.GET()

    def PUT(self):
        return self.GET()

    def DELETE(self):
        return self.GET()


@template("error/401", "401 UNAUTHORIZED")
class error401(MixedObject):
    @HTML
    def GET(self):
        return Response(401, [("Content-Type", "text/html")], self.view.render())

    def POST(self):
        return self.GET()

    def PUT(self):
        return self.GET()

    def DELETE(self):
        return self.GET()


@template("error/500", "500 INTERNAL SERVER ERROR")
class error500(MixedObject):
    @HTML
    def GET(self):
        self.view.data = {
            "error": self.request.errors.exception,
            "tb": self.request.errors.traceback
        }
        return Response(500, [("Content-Type", "text/html")], self.view.render())

    def POST(self):
        return self.GET()

    def PUT(self):
        return self.GET()

    def DELETE(self):
        return self.GET()
