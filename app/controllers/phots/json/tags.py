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
from seshat.baseObject import JSONObject

import models.rethink.phot.photModel as pm
import rethinkdb as r


@autoRoute()
class tags(JSONObject):
    def GET(self):
        hidden_ids = list(r.table(pm.Phot.table)\
            .filter(r.row["disable"].eq(True))\
            .concat_map(lambda doc: [doc["id"]]).run())

        base_query = r.table(pm.Phot.table)\
            .filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"]))

        raw_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        all_tags = []

        for tag in raw_tags:
            res = {
                "value": tag.replace("_", " "),
                "tokens": tag.split("_")
            }
            all_tags.append(res)

        return all_tags
