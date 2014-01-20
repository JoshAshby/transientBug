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
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import login
from seshat_addons.func_mods import JSON


@route()
@login(["admin"])
class toggle(MixedObject):
    @JSON
    def POST(self):
        self.request.announcements.toggle_announcement(self.request.id)
        return {"success": True, "id": self.request.id}
