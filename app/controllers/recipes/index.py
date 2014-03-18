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
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.recipe.recipeModel as rm


@route()
@template("public/recipes/index", "Recipes")
class index(MixedObject):
    @HTML
    def GET(self):
        #parts = r.table(rm.Recipe.table).filter({"disable": False,
                                                 #"public": True})

        #result = RethinkCollection(rm.Recipe, query=parts)
        result = RethinkCollection(rm.Recipe)
        page = Paginate(result, self.request, "created", sort_direction_default="asc")

        self.view.data = {"recipes": page}

        return self.view
