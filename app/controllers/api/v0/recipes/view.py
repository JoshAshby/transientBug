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


@route()
class view(MixedObject):
    @JSON
    def GET(self):
        recipe = None
        if len(self.request.id) == 10:
            recipe = rm.Recipe.find(self.request.id)

        elif len(self.request.id) == 36:
            recipe = rm.Recipe(self.request.id)

        if recipe is None:
            return NotFound()

        if recipe.user.id != self.session.id:
            return Unauthorized()

        if not recipe.public:
          if not self.session.id or self.session.id!=recipe.user:
                self.session.push_alert("That recipe is not public and you do not have the rights to access it.", level="error")
                return Unauthorized()

        if recipe.deleted:
            return NotFound()

        return recipe
