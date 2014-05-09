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
from seshat_addons.seshat.obj_mods import template, login
from seshat_addons.seshat.func_mods import HTML

from utils.paginate import Paginate

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.recipe.recipeModel as rm


@route()
@login(["recipes"])
@template("public/recipes/yours", "Recipes")
class yours(MixedObject):
    @HTML
    def GET(self):
        d = self.request.get_param("d")
        p = self.request.get_param("p")
        parts = {
            "deleted": False,
            "user": self.session.id
        }

        if d:
            parts["deleted"] = True

        if not ("public" in p and "private" in p):
            if "public" in p:
                parts["public"] = True

            elif "private" in p:
                parts["public"] = False

        parts = r.table(rm.Recipe.table).filter(parts)

        result = RethinkCollection(rm.Recipe, query=parts)
        page = Paginate(result, self.request, "title", sort_direction_default="desc")

        return {"recipes": page}
