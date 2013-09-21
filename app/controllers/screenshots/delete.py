#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c

from seshat.route import autoRoute
from seshat.baseObject import JSONObject
from seshat.objectMods import login


@login(["root"])
@autoRoute()
class delete(JSONObject):
    """
    allows for the deletion of an screenshot
    """
    def POST(self):
        current_path = ''.join([c.general.dirs["screenshots"], self.request.id])

        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break

        if self.request.id in f:
            os.remove(current_path)

            self.request.session.pushAlert("Deleting screenshot...")
            return {"success": True}

        else:
            raise Exception("That image could not be found.")
