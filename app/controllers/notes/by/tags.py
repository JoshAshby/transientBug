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
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm

import models.utils.dbUtils as dbu


@autoRoute()
class tags(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/by/tags"
    def GET(self):
        """
        """
        tag = self.request.id or self.request.getParam("q")
        query = tag.replace("_", " ")

        parts = r.table(nm.Note.table).filter({"disable": False})

        if self.request.session.userID:
            what_type = self.request.getParam("filter", "all")

            if what_type=="private":
                parts = parts.filter({"public": False})
            elif what_type=="public":
                parts = parts.filter({"public": True})

        else:
            parts = parts.filter({"public": True})

        all_tags = parts.concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        all_tags.sort()

        if query:
            try:
                similar, top = dbu.search_tags(all_tags, query)
            except Exception:
                self.view.template = "public/notes/errors/no_matching_tags"
                self.view.data = {"tag": query}
                return self.view

            parts = parts.filter(r.row["tags"]\
                .filter(lambda t: t == top ).count() > 0)
            result = RethinkCollection(nm.Note, query=parts)
            page = Paginate(result, self.request, "created", sort_direction="asc")

            if page.pail:
                self.view.data = {"page": page,
                                  "type": what_type.lower(),
                                  "tags": similar,
                                  "tag": top,
                                  "q": query}
                return self.view

            else:
                self.view.template = "public/notes/errors/empty_tag"
                self.view.data = {"tag": top}
                return self.view

        else:
            if not all_tags:
                self.view.template = "public/notes/errors/tags"
                return self.view

            self.view.template = "public/common/tags"
            self.view.data = {"tags": all_tags,
                              "nav": {"notes": True},
                              "where": "notes/by",
                              "theme_color": "red",
                              "type": "Notes"}
            return self.view
