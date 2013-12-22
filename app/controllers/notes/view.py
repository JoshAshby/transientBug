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
from seshat.actions import NotFound, Unauthorized

import rethinkdb as r
import models.rethink.note.noteModel as nm


@autoRoute()
class view(MixedObject):
    _title = "note"
    _default_tmpl = "public/notes/view"
    def GET(self):
        """
        """
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id, "disable": False})\
            .coerce_to('array').run()

        if f:
            note = nm.Note(**f[0])

            if not note.public and (not self.request.session.userID \
                      or self.request.session.userID!=note.user):
                    self.request.session.pushAlert("That note is not public and you do not have the rights to access it.", level="error")
                    return Unauthorized()

            if self.request.session.has_notes:
                self.view.scripts = ["note"]

            if self.request.session.userID:
                if note.public:
                    title = """<i class="icon-eye-open"></i> """
                else:
                    title = """<i class="icon-eye-close"></i> """

                title += note.title
            else:
                title = note.title

            self.view.data = {"note": note, "header": title}
            return self.view

        else:
            self.request.session.pushAlert("That note could not be found!", level="error")
            return NotFound()
