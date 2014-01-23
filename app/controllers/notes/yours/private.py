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
from seshat_addons.obj_mods import template, login
from seshat_addons.func_mods import HTML

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm


@route()
@login(["notes"])
@template("public/notes/index", "Notes")
class private(MixedObject):
    @HTML
    def GET(self):
        parts = r.table(nm.Note.table).filter({"disable": False, "public":
          False, "draft": False, "user": self.request.session.id})

        result = RethinkCollection(nm.Note, query=parts)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view
