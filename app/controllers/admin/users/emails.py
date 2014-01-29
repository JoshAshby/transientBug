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
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML

from seshat.actions import NotFound

from errors.general import NotFoundError

from models.rethink.user import userModel as um

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.email.emailModel as em
from utils.paginate import Paginate


@route()
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

        t = self.request.get_param("filter", "to")
        if t == "cc":
            row_filt = "cc_addresses"
        elif t == "bcc":
            row_filt = "bcc_addresses"
        else:
            row_filt = "to_addresses"

        parts = r.table(em.Email.table).filter(lambda row: row[row_filt].contains(user.id))

        result = RethinkCollection(em.Email, query=parts)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page,
                          "user": user,
                          "command": self.request.command}

        return self.view
