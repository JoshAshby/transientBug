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
from seshat.objectMods import template
from seshat.funcMods import HTML


@autoRoute()
@template("public/about/about", "About")
class about(MixedObject):
    @HTML
    def GET(self):
        return self.view
