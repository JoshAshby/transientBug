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
class public(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        perpage = self.request.getParam("perpage", 25)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")

        f = []
        if sort_dir.lower() == "desc":
            sort = r.desc("created")
        else:
            sort = "created"

        parts = r.table(nm.Note.table).order_by(sort).filter({"public": True})

        for part in parts.run():
            note = nm.Note.fromRawEntry(**part)
            note.format()
            f.append(note)

        f, page_dict = pager(f, perpage, page)

        self.view.data = {"notes": f, "page": page_dict, "dir": sort_dir.lower()}
        return self.view
