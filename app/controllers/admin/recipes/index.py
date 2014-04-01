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
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.recipe.recipeModel as rm
from utils.paginate import Paginate

from searchers.recipes import RecipeSearcher
import whoosh.query as q


@route()
@login(["admin"])
@template("admin/recipes/index", "Recipes")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "recipes"})

        deleted = self.request.get_param("d", False)
        reported = self.request.get_param("r", False)
        public = self.request.get_param("p", False)
        search = self.request.get_param("s")

        if not search:
            parts = {}

            if deleted:
                parts["deleted"] = True

            if reported:
                parts["reported"] = True

            if public:
                parts["public"] = True

            query = r.table(rm.Recipe.table).filter(parts)
            res = RethinkCollection(rm.Recipe, query=query)

        else:
            pass

        page = Paginate(res, self.request, "title", sort_direction_default="desc")

        return {"recipes": page}
