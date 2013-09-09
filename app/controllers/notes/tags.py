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
from seshat.objectMods import login

from utils.paginate import pager

import rethinkdb as r
import models.rethink.note.noteModel as nm


#@login(["notes"])
@autoRoute()
class tags(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        tag = self.request.id

        perpage = self.request.getParam("perpage", 25)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")
        what_type = self.request.getParam("filter", "all")

        f = []
        if sort_dir.lower() == "desc":
            sort = r.desc("created")
        else:
            sort = "created"

        parts = r.table(nm.Note.table).order_by(sort).filter(r.row['tags'].filter(lambda el: el == tag).count() > 0)

        if not self.request.session.has_notes:
            parts = parts.filter({"public": True})

        else:
            parts = parts.filter({"user": self.request.session.userID})
            if what_type=="private":
                parts = parts.filter({"public": False})
            elif what_type=="public":
                parts = parts.filter({"public": True})

        for part in parts.run():
            note = nm.Note.fromRawEntry(**part)
            note.format()
            f.append(note)

        f, page_dict = pager(f, perpage, page)

        self.view.data = {"notes": f, "page": page_dict, "dir": sort_dir.lower(), "type": what_type.lower()}
        return self.view
