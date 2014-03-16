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
from seshat_addons.seshat.func_mods import JSON

import rethinkdb as r
import models.rethink.recipe.recipeModel as rm


@route()
class tags(MixedObject):
    @JSON
    def GET(self):
        base_query = r.table(rm.Recipe.table).filter({"disable": False,
                                                      "reported": False,
                                                      "public": True})

        raw_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        return {"tags": raw_tags}
