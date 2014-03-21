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
from utils.paginate import Paginate
from seshat_addons.seshat.func_mods import JSON

from rethinkORM import RethinkCollection
import models.rethink.recipe.recipeModel as rm
import rethinkdb as r

@route()
class index(MixedObject):
    @JSON
    def GET(self):
        query = r.table(rm.Recipe.table).filter({"deleted": False,
                                                 "reported": False,
                                                 "public": True})

        res = RethinkCollection(rm.Recipe, query=query)

        page = Paginate(res, self.request, "name", sort_direction_default="desc")

        return page
