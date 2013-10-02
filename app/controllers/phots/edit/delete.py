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


@login(["phots"])
@autoRoute()
class delete(JSONObject):
    """
    allows for the renaming of an image
    """
    def POST(self):
        current = list(r.table(pm.Phot.table).filter({"filename": self.request.id}).run())
        if current:
            current = pm.Phot(current[0]["id"])
            current.disable = True
            current.save()

            return {"success": True}

        else:
            return {"success": False, "error": "That image couldn't be found. :/"}
