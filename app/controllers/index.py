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


@autoRoute()
class index(MixedObject):
    _title = "Home"
    _default_tmpl = "public/index/index"
    def GET(self):
        if self.request.session.id:
            return self.view
        else:
            return Redirect("/phots")
