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

from fuzzywuzzy import fuzz


@autoRoute()
class tags(HTMLObject):
    """
    """
    _title = "notes"
    _defaultTmpl = "public/notes/by/tags"
    def GET(self):
        """
        """
        tag = self.request.id
        query = self.request.getParam("q")

        if not query and tag: query = tag

        query = query.replace("_", " ")

        parts = r.table(nm.Note.table).filter({"disable": False})

        if self.request.session.userID:
            what_type = self.request.getParam("filter", "all")

            if what_type=="private":
                parts = parts.filter({"public": False})
            elif what_type=="public":
                parts = parts.filter({"public": True})

        else:
            parts = parts.filter({"public": True})

        tags = list(parts.concat_map(lambda doc: doc["tags"]).run())

        if query:
            new_tags = {}
            for t in tags:
                match = fuzz.partial_ratio(query, t.replace("_", " "))
                if match >= 85:
                    new_tags[t] = match

            tags = new_tags.copy().keys()
            try:
                tag = max(new_tags, key=new_tags.get)
            except ValueError:
                self.view.template = "public/notes/errors/no_matching_tags"
                self.view.data = {"tag": query}
                return self.view

            self.view.data = {"q": query}

            parts = parts.filter(r.row["tags"].filter(lambda t: t == tag ).count() > 0)

            result = RethinkCollection(nm.Note, query=parts)
            page = Paginate(result, self.request, "created", sort_direction="asc")

            if page.pail:
                self.view.data = {"page": page,
                                  "type": what_type.lower(),
                                  "tags": tags,
                                  "tag": tag,}
                return self.view

            else:
                self.view.template = "public/notes/errors/empty_tag"
                self.view.data = {"error": "There are not any notes with the tag: %s!" % tag}
                return self.view

        else:
            if not tags:
                self.view.template = "public/notes/errors/tags"
                return self.view

            tags = list(set([ item.replace("_", " ") for item in tags ]))

            self.view.template = "public/common/tags"
            self.view.data = {"tags": tags, "nav": {"notes": True}, "where": "notes/by", "theme_color": "red", "type": "Notes"}
            return self.view
