#!/usr/bin/env python
"""
main index listing for notes - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import template
from seshat_addons.func_mods import HTML

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm


@route()
@template("public/notes/index", "Notes")
class index(MixedObject):
    @HTML
    def GET(self):
        parts = r.table(nm.Note.table).filter({"disable": False, "public": True, "draft": False})

        result = RethinkCollection(nm.Note, query=parts)
        page = Paginate(result, self.request, "created")

        self.view.partial("note_list", "partials/public/notes/list",
                          {"page": page})

        self.view.data = {"page": page}

        return self.view
