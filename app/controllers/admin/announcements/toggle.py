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
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login
from seshat_addons.seshat.func_mods import JSON


@route()
@login(["admin"])
class toggle(MixedObject):
    @JSON
    def POST(self):
        state = self.request.get_param("state", None, cast=bool)
        new_state = self.request.announcements.toggle_announcement(self.request.id, state)

        success = False
        if state is None:
            success = True
        elif state == new_state:
            success = True

        return {"success": success, "id": self.request.id, "state": new_state}
