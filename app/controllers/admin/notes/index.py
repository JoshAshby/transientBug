#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.MixedObject import MixedObject
from seshat_addons.objectMods import login, template
from seshat_addons.funcMods import HTML

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
from utils.paginate import Paginate
import models.utils.dbUtils as dbu


@route()
@login(["admin"])
@template("admin/notes/index", "Notes")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "notes"})

        what_type = self.request.get_param("filter", "all")

        parts = {}

        if what_type=="private":
            parts["public"] = False
        elif what_type=="public":
            parts["public"] = True

        self.view.data = {"type": what_type.lower()}

        disabled = self.request.get_param("q")
        if disabled != "enabled":
            q = dbu.rql_where_not(nm.Note.table, "disable", True, parts)
            res = RethinkCollection(nm.Note, query=q)

        else:
            q = r.table(nm.Note.table).filter(parts)
            res = RethinkCollection(nm.Note, query=q)

        page = Paginate(res, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view
