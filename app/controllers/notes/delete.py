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
from seshat.actions import Unauthorized, NotFound

import rethinkdb as r
import models.rethink.note.noteModel as nm


@route()
@login(["notes"])
class delete(MixedObject):
    @JSON
    def POST(self):
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to("array").run()

        if f:
            note = nm.Note(**f[0])
            if note.author.id != self.request.session.id:
                self.request.session.push_alert("You don't own that note, you can't delete it!", level="danger")
                return Unauthorized()

            note.disable = True
            note.save()
            return {"success": True}

        else:
            return NotFound()
