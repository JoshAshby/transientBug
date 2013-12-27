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
from seshat.MixedObject import MixedObject
from seshat.objectMods import login

from seshat.actions import NotFound, Redirect

from errors.general import NotFoundError

from models.rethink.user import userModel as um

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
from utils.paginate import Paginate


@login(["admin"])
@autoRoute()
class notes(MixedObject):
    _title = "Users"
    _default_tmpl = "admin/users/notes"
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

        parts = r.table(nm.Note.table).filter({"user": self.request.session.id})

        what_type = self.request.getParam("filter", "all")

        if what_type=="private":
            parts = parts.filter({"public": False})
        elif what_type=="public":
            parts = parts.filter({"public": True})

        self.view.data = {"type": what_type.lower()}

        result = RethinkCollection(nm.Note, query=parts)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view
