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
from seshat.actions import Unauthorized, NotFound

import rethinkdb as r
import models.rethink.note.noteModel as nm
from searchers.notes import NoteSearcher


@route("/notes/:id/delete")
@login(["notes"])
class delete(MixedObject):
    @JSON
    def POST(self):
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to("array")\
            .run()

        if f:
            note = nm.Note(**f[0])
            if not self.session.has_group("admin")\
                or note.author.id != self.session.id:
                self.session.push_alert("You don't own that note, you can't delete it!",
                                        level="error")
                return Unauthorized()

            note.disable = True
            note.save()

            searcher = NoteSearcher()
            searcher.update(note)
            searcher.save()

            return {"success": True}

        else:
            return NotFound()
