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
from seshat_addons.seshat.func_mods import HTML, JSON

import models.rethink.recipe.recipeModel as rm


@route()
@login(["recipes"])
@template("public/recipes/new", "New Recipe")
class new(MixedObject):
    @HTML
    def GET(self):
        return self.view

    @JSON
    def POST(self):
        try:
            name = self.request.get_param("name")
            tags = self.request.get_param("tags")
            ingredients = self.request.get_param("ingredients")
            steps = self.request.get_param("steps")

            recipe = rm.Recipe.new_recipe(self.request.session.id,
                               title=name,
                               ingredients=ingredients,
                               steps=steps,
                               tags=tags)

            print recipe

            return {"success": True}
        except Exception as e:
            print e
