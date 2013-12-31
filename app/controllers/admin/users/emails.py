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
from seshat.objectMods import login, template
from seshat.funcMods import HTML

from seshat.actions import NotFound

from errors.general import NotFoundError

from models.rethink.user import userModel as um

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.email.emailModel as em
from utils.paginate import Paginate


@autoRoute()
@login(["admin"])
@template("admin/users/emails", "User Emails")
class emails(MixedObject):
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

        parts = r.table(em.Email.table).filter(lambda row: row["users"].contains(user.id))

        result = RethinkCollection(em.Email, query=parts)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view
