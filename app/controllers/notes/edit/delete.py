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

import rethinkdb as r
import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class delete(JSONObject):
    """
    allows for the deletion of an screenshot
    """
    def POST(self):
        note = self.request.id

        f = r.table(nm.Note.table).filter({"short_code": note}).run()

        f = list(f)
        if f:
            f = f[0]

            note = nm.Note(**f)

            try:
                note.disable = True

                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}

        else:
            return {"success": False, "error": "That note couldn't be found. :/"}
