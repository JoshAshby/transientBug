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

from utils.paginate import rethink_pager

import rethinkdb as r
import models.rethink.note.noteModel as nm


@autoRoute()
class index(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        if not self.request.session.has_notes:
            self._redirect("/notes/public")
            return

        what_type = self.request.getParam("filter", "all")
        view = self.request.getParam("v", "cards")

        parts = r.table(nm.Note.table).filter({"user": self.request.session.userID})

        if what_type=="private":
            parts = parts.filter({"public": False})
        elif what_type=="public":
            parts = parts.filter({"public": True})

        f, pager_dict = rethink_pager(parts, self.request, "created")

        if f:
            new_f = []
            for part in f:
                note = nm.Note.fromRawEntry(**part)
                note.format()
                new_f.append(note)

            data = {"notes": new_f, "page": pager_dict, "type": what_type.lower()}
            data[view] = True

            self.view.data = data

            return self.view

        else:
            self.view.template = "public/notes/error"
            self.view.data = {"error": "No notes have been written yet!"}
            return self.view
