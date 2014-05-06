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

import rethinkdb as r

from rethinkORM import RethinkCollection
from utils.paginate import Paginate

from models.rethink.user import userModel as um
from models.rethink.email import emailModel as em


@route()
@login()
@template("public/account/emails", "Emails")
class emails(MixedObject):
    @HTML
    def GET(self):
        user = um.User(self.session.id)

        t = self.request.get_param("filter", "to")
        if t == "cc":
            row_filt = "cc_addresses"
        elif t == "bcc":
            row_filt = "bcc_addresses"
        else:
            row_filt = "to_addresses"

        parts = r.table(em.Email.table).filter(lambda row: row[row_filt].contains(user.id))

        result = RethinkCollection(em.Email, query=parts)
        page = Paginate(result, self.request, "created", sort_direction_default="asc")

        self.view.data = {"user": user, "page": page, "command": "emails"}

        return self.view
