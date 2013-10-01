#!/usr/bin/env python
"""
main index listing for notes - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject

from utils.paginate import Paginate

import rethinkdb as r
import models.rethink.note.noteModel as nm


@autoRoute()
class public(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        parts = r.table(nm.Note.table).filter({"public": True})

        page = Paginate(parts, self.request, "created")
        f = page.pail

        if f:
            new_f = []
            for part in f:
                note = nm.Note(**part)
                note.format()
                new_f.append(note)

            self.view.data = {"notes": new_f, "page": page}
            return self.view

        else:
            self.view.template = "public/notes/error"
            self.view.data = {"error": "There are not any publicly visible notes yet!"}
            return self.view
