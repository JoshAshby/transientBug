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

import models.utils.dbUtils as dbu
import models.rethink.phot.photModel as pm


@autoRoute()
class json(MixedObject):
    def GET(self):
        base_query = dbu.rql_where_not(pm.Phot.table, "disable", True)

        raw_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        all_tags = []

        for tag in raw_tags:
            res = {
                "value": tag,
                "tokens": tag.replace("_", " ").split(" ")
            }
            all_tags.append(res)

        return {"tags": all_tags}
