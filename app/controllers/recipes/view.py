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
from seshat.actions import NotFound, Unauthorized, Redirect
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template, login
from seshat_addons.seshat.func_mods import HTML

import models.rethink.recipe.recipeModel as rm
import searchers.recipes as rs


@route()
@login(["recipes"])
@template("public/recipes/view", "Recipe")
class view(MixedObject):
    @HTML
    def GET(self):
        recipe = rm.Recipe.find(self.request.id)

        if recipe is None:
            return NotFound()

        if recipe.user.id is not self.request.session.id:
            if not recipe.public:
                return Unauthorized()

        self.view.title = recipe.title
        return {"recipe": recipe}

    @HTML
    def POST(self):
        recipe = rm.Recipe.find(self.request.id)

        if recipe is None:
            return NotFound()

        if recipe.user.id is not self.request.session.id:
            if not recipe.public:
                return Unauthorized()

        recipe.title = self.request.get_param("title")
        recipe.tags = self.request.get_param("tags")
        recipe.public = self.request.get_param("public", False)
        recipe.country = self.request.get_param("country")
        recipe.description = self.request.get_param("description")
        recipe.ingredients = self.request.get_param("ingredients")
        recipe.steps = self.request.get_param("steps")

        recipe.save()

        searcher = rs.RecipeSearcher()
        searcher.update(recipe)
        searcher.save()

        return Redirect("/recipes/{}".format(self.request.id))
