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
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

import rethinkdb as r
import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class view(HTMLObject):
    """
    """
    _title = "note"
    _defaultTmpl = "public/notes/view"
    def GET(self):
        """
        """
        note = self.request.id

        f = r.table(nm.Note.table).filter({"note_code": note}).run()

        print f

        self.view.data = {"note": f}
        return self.view
