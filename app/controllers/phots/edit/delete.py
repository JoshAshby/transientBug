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

import models.rethink.phot.photModel as pm
import rethinkdb as r


@login(["phots"])
@autoRoute()
class delete(JSONObject):
    """
    allows for the renaming of an image
    """
    def POST(self):
        current_path = ''.join([c.general.dirs["gifs"], self.request.id])

        f = []
        for top, folders, files in os.walk(c.general.dirs["gifs"]):
            f.extend(files)
            break

        if self.request.id in f:
            try:
                f = r.table(pm.Phot.table).filter({"filename": self.request.id}).run()
                f = list(f)
                if len(f):
                    photo = pm.Phot(**f[0])
                    photo.delete()
                    os.remove(current_path)

                    return {"success": True}

                else:
                    return {"success": False, "error": "Could not find photo in db"}

            except Exception as e:
                return {"success": False, "error": str(e)}

        else:
            return {"success": False, "error": "That image couldn't be found. :/"}
