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

from utils.paginate import rethink_pager

import rethinkdb as r
import models.rethink.note.noteModel as nm


@autoRoute()
class tags(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/index"
    def GET(self):
        """
        """
        tag = self.request.id

        if tag:
            perpage = self.request.getParam("perpage", 25)
            page = self.request.getParam("page", 0)
            sort_dir = self.request.getParam("dir", "desc")
            what_type = self.request.getParam("filter", "all")

            parts = r.table(nm.Note.table).filter(r.row['tags'].filter(lambda el: el == tag).count() > 0)

            if not self.request.session.has_notes:
                parts = parts.filter({"public": True})

            else:
                parts = parts.filter({"user": self.request.session.userID})
                if what_type=="private":
                    parts = parts.filter({"public": False})
                elif what_type=="public":
                    parts = parts.filter({"public": True})

            f, pager_dict = rethink_pager(parts, perpage, page, sort_dir, "created")

            if f:
                new_f = []
                for part in f:
                    note = nm.Note.fromRawEntry(**part)
                    note.format()
                    new_f.append(note)

                self.view.data = {"notes": new_f, "page": pager_dict, "type": what_type.lower(), "tag": tag}
                return self.view

            else:
                self.view.template = "public/notes/error"
                self.view.data = {"error": "There are not any notes with the tag: %s!" % tag}
                return self.view

        else:
            tags = list(r.table(nm.Note.table).concat_map(lambda doc: doc["tags"]).run())

            if not tags:
                self.view.template = "public/notes/error"
                self.view.data = {"error": "We do not currently have any tags within the system!"}
                return self.view

            self.view.template = "public/notes/tags"
            self.view.data = {"tags": tags}
            return self.view
