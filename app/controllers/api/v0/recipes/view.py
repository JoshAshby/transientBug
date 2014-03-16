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
from seshat.actions import NotFound, Unauthorized
from seshat_addons.seshat.func_mods import JSON

import models.rethink.recipe.recipeModel as rm
import rethinkdb as r


@route()
class view(MixedObject):
    @JSON
    def GET(self):
        f = r.table(rm.Recipe.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to('array').run()

        if f:
            recipe = rm.Recipe(**f[0])

            if not recipe.public:
              if not self.request.session.id or self.request.session.id!=recipe.user:
                    self.request.session.push_alert("That recipe is not public and you do not have the rights to access it.", level="error")
                    return Unauthorized()

            if not self.request.session.has_recipes and recipe.disable:
                return NotFound()

            return recipe

        else:
            return NotFound()
