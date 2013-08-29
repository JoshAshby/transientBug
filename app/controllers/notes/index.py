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

import rethink as r
import models.rethink.note.noteModel as nm


@login(["root"])
@autoRoute()
class index(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")

        f = []
        parts = r.table("notes").run()
        for part in parts:
            f.append(nm.fromRawEntry)

        f, page_dict = pager(f, perpage, page, sort_dir)

        self.view.data = {"notes": f, "page": page_dict}
        return self.view
