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
from seshat_addons.MixedObject import MixedObject
from seshat_addons.objectMods import template
from seshat_addons.funcMods import HTML


@route()
@template("public/about/about", "About")
class about(MixedObject):
    @HTML
    def GET(self):
        return self.view
