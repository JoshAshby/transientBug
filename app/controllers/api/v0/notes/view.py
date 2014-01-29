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
from seshat.actions import NotFound, Unauthorized
from seshat_addons.seshat.func_mods import JSON

import models.rethink.note.noteModel as nm
import rethinkdb as r


@route()
class view(MixedObject):
    @JSON
    def GET(self):
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to('array').run()

        if f:
            note = nm.Note(**f[0])

            if not note.public:
              if not self.request.session.id or self.request.session.id!=note.user:
                    self.request.session.push_alert("That note is not public and you do not have the rights to access it.", level="error")
                    return Unauthorized()

            if not self.request.session.has_notes and note.disable:
                return NotFound()

            return note.for_json()


        else:
            return NotFound()
