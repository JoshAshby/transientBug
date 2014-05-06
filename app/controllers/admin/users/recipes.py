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

from seshat.actions import NotFound

from errors.general import NotFoundError

from models.rethink.user import userModel as um

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.recipe.recipeModel as rm
from utils.paginate import Paginate


@route("/admin/users/:id/recipes")
@login(["admin"])
@template("admin/users/recipes", "User Recipes")
class recipes(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "users"})
        try:
            user = um.User(self.request.id)

        except NotFoundError:
            return NotFound()

        self.view.title = user.username

        deleted = self.request.get_param("d", False)
        reported = self.request.get_param("r", False)

        parts = {"user": user.id}

        if deleted:
            parts["deleted"] = True

        if reported:
            parts["reported"] = True

        query = r.table(rm.Recipe.table).filter(parts)
        res = RethinkCollection(rm.Recipe, query=query)
        page = Paginate(res, self.request, "title", sort_direction_default="desc")

        return {"recipes": page,
                "user": user,
                "command": "recipes"}
