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
from seshat.baseObject import JSONObject
from seshat.objectMods import login

import models.rethink.phot.photModel as pm
import rethinkdb as r


@login(["admin"])
@autoRoute()
class toggle(JSONObject):
    def POST(self):
        current = pm.Phot(self.request.id)

        if current.filename:
            current.disable = not current.disable if "disable" in current._data else True
            current.save()

            return {"success": True}

        else:
            return {"success": False, "error": "That image couldn't be found. :/"}
