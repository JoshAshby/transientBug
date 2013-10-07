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
from seshat.actions import Redirect

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm


@autoRoute()
class index(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        parts = r.table(nm.Note.table).filter({"disable": False})

        if self.request.session.userID:
            what_type = self.request.getParam("filter", "all")

            if what_type=="private":
                parts = parts.filter({"public": False})
            elif what_type=="public":
                parts = parts.filter({"public": True})

            self.view.data = {"type": what_type.lower()}

        else:
            parts = parts.filter({"public": True})

        result = RethinkCollection(nm.Note, query=parts)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        if page.pail:
            data = {"page": page}

            self.view.data = data

            return self.view

        else:
            if self.request.session.userID:
                return Redirect("/notes/new")

            self.view.template = "public/notes/errors/empty"
            return self.view
