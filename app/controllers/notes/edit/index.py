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
from seshat.actions import Redirect, NotFound

import rethinkdb as r
import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class index(MixedObject):
    _title = "note"
    _default_tmpl = "public/notes/edit"
    def GET(self):
        f = list(r.table(nm.Note.table).filter({"short_code": self.request.id}).run())

        if f:
            note = nm.Note(**f[0])

            tags = ', '.join(note.tags)

            self.view.data = {"note": note, "tags": tags}
            return self.view

        else:
            self.request.session.push_alert("That note could not be found!", level="error")
            return NotFound()

    def POST(self):
        title = self.request.getParam("title")
        contents = self.request.getParam("contents")
        public = self.request.getParam("public", False)
        tags = self.request.getParam("tags")

        tag = []
        if tags:
            tag = [ bit.lstrip().rstrip() for bit in tags.split(",") ]

        f = list(r.table(nm.Note.table).filter({"short_code": self.request.id}).run())

        if f:
            note = nm.Note(**f[0])

            if note.user != self.request.session.id:
                note.copy()

            note.title = title
            note.contents = contents
            note.public = public
            note.tags = tag

            note.save()

        else:
            return NotFound()

        return Redirect("/notes/%s" % note.short_code)
