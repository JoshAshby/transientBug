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
from seshat.actions import NotFound

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
import models.rethink.user.userModel as um


@autoRoute()
class user(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        user = self.request.id

        u = list(r.table(um.User.table).filter({"username": user}).run())

        if u:
            user_id = u[0]["id"]

            parts = r.table(nm.Note.table).filter({"public": True, "user": user_id})
            result = RethinkCollection(nm.Note, query=parts)
            page = Paginate(result, self.request, "created")

            if page.pail:
                self.view.data = {"page": page, "user": user}
                return self.view

            else:
                self.view.template = "public/notes/errors/no_public"
                self.view.data = {"user": user}
                return self.view

        else:
            return NotFound()
