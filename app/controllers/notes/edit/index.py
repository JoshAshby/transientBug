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
from seshat.actions import Redirect, NotFound, Unauthorized

import rethinkdb as r
import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class index(MixedObject):
    _title = "note"
    _default_tmpl = "public/notes/edit"
    def GET(self):
        self.view.partial("sidebar", "partials/public/notes/sidebar_links")
        f = list(r.table(nm.Note.table).filter({"short_code": self.request.id}).run())

        if f:
            note = nm.Note(**f[0])
            if note.author.id is not self.request.session.id:
                self.request.session.push_alert("You don't own that note, you can't edit it!", level="danger")
                return Unauthorized()

            tags = ', '.join(note.tags)

            self.view.data = {"note": note, "tags": tags}
            return self.view

        else:
            return NotFound()

    def POST(self):
        title = self.request.getParam("title")
        contents = self.request.getParam("contents")
        public = self.request.getParam("public", False)
        tags = self.request.getParam("tags")

        tag = []
        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in tags.split(",") ]

        f = list(r.table(nm.Note.table).filter({"short_code": self.request.id}).run())

        if f:
            note = nm.Note(**f[0])
            if note.author.id is not self.request.session.id:
                self.request.session.push_alert("You don't own that note, you can't edit it!", level="danger")
                return Unauthorized()

            note.title = title
            note.contents = contents
            note.public = public
            note.tags = tag

            note.save()

        else:
            return NotFound()

        return Redirect("/notes/%s" % note.short_code)
