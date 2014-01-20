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
from seshat_addons.objectMods import login
from seshat_addons.funcMods import JSON


@route()
@login(["admin"])
class toggle(MixedObject):
    @JSON
    def POST(self):
        self.request.announcements.toggle_announcement(self.request.id)
        return {"success": True, "id": self.request.id}
