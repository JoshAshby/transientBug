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
from seshat.objectMods import login
from seshat.funcMods import JSON


@autoRoute()
@login(["admin"])
class toggle(MixedObject):
    @JSON
    def POST(self):
        self.request.announcements.toggle_announcement(self.request.id)
        return {"success": True, "id": self.request.id}
