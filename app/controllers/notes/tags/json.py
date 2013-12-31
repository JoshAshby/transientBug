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
from seshat.funcMods import JSON

import models.utils.dbUtils as dbu
import models.rethink.note.noteModel as nm


@autoRoute()
class json(MixedObject):
    @JSON
    def GET(self):
        base_query = dbu.rql_where_not(nm.Note.table, "disable", True)

        raw_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        all_tags = []

        for tag in raw_tags:
            res = {
                "value": tag.replace("_", " "),
                "tokens": tag.replace("_", " ").split(" ")
            }
            all_tags.append(res)

        return {"tags": all_tags}
