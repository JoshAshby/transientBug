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
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id, "disable": False})\
            .coerce_to('array').run()

        if f:
            note = nm.Note(**f[0])

            if not note.public and (not self.request.session.id \
                      or self.request.session.id!=note.user):
                    self.request.session.push_alert("That note is not public and you do not have the rights to access it.", level="error")
                    return Unauthorized()

            if self.request.session.id:
                if note.public:
                    title = """<i class="fa fa-eye"></i> """
                else:
                    title = """<i class="fa fa-eye-slash"></i> """

                title += note.title
            else:
                title = note.title

            title = "<h1>{}</h1>".format(title)

            self.view.data = {"note": note, "header": title}
            return self.view

        else:
            return NotFound()
