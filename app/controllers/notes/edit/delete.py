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

import rethinkdb as r
import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class delete(MixedObject):
    def POST(self):
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to("array").run()

        if f:
            note = nm.Note(**f[0])
            note.disable = True
            note.save()
            return {"success": True}

        else:
            return {"success": False,
                    "error": "That note couldn't be found. :/"}
