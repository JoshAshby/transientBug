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

from seshat.actions import NotFound

from errors.general import NotFoundError

from models.rethink.user import userModel as um

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
from utils.paginate import Paginate
import models.utils.dbUtils as dbu


@route()
@login(["admin"])
@template("admin/users/notes", "User Notes")
class notes(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "users"})
        try:
            user = um.User(self.request.id)

        except NotFoundError:
            return NotFound()

        self.view.title = user.username

        self.view.partial("tabs",
                          "partials/admin/users/tabs",
                          {"user": user,
                           "command": self.request.command})

        parts = {"user": self.request.session.id}

        what_type = self.request.get_param("filter", "all")

        if what_type=="private":
            parts["public"] = False
        elif what_type=="public":
            parts["public"] = True

        self.view.data = {"type": what_type.lower()}

        disabled = self.request.get_param("q")
        if disabled == "enabled":
            q = dbu.rql_where_not(nm.Note.table, "disable", True, parts)
            res = RethinkCollection(nm.Note, query=q)

        else:
            q = dbu.rql_where_not(nm.Note.table, "disable", False, parts)
            res = RethinkCollection(nm.Note, query=q)

        page = Paginate(res, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view
