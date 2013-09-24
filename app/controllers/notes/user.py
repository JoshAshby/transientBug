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

from utils.paginate import Paginate

import rethinkdb as r
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
            u = u[0]

            user_id = u["id"]

            parts = r.table(nm.Note.table).filter({"public": True, "user": user_id})

            page = Paginate(parts, self.request, "created")
            f = page.pail

            if f:
                new_f = []
                for part in f:
                    note = nm.Note.fromRawEntry(**part)
                    note.format()
                    new_f.append(note)

                self.view.data = {"notes": new_f, "page": page, "user": user}
                return self.view

            else:
                self.view.template = "public/notes/error"
                self.view.data = {"error": "The user: %s has not written any notes yet!" % user}
                return self.view

        else:
            self.view.template = "public/notes/error"
            self.view.data = {"error": "The user: %s does not exist in the system yet" % user}
            return self.view
