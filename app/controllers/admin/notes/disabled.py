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
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import login, template
from seshat_addons.func_mods import HTML

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/notes/index", "Notes")
class disabled(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "notes"})

        q = r.table(nm.Note.table).filter({"disable": True})
        res = RethinkCollection(nm.Note, query=q)

        page = Paginate(res, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page, "enabled": False}

        return self.view
