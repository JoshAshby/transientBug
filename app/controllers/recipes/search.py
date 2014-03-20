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
import models.rethink.recipe.recipeModel as rm
from searchers.recipes import RecipeSearcher


@route()
@login(["recipes"])
@template("public/recipes/search/index", "Search Recipes")
class search(MixedObject):
    @HTML
    def GET(self):
        search_term = self.request.get_param("s")

        all_tags = r.table(rm.Recipe.table)\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        self.view.data = {"tags": all_tags, "recipes": None}

        if search_term:
            search_term = search_term.replace("tag:", "tags:")

            searcher = RecipeSearcher()
            parts = {"deleted": False, "public": True}

            ids = searcher.search(search_term, collection=True)
            if ids is not None:
                ids.filter(parts)
                ids.fetch()

                page = Paginate(ids, self.request, "created", sort_direction_default="asc")
                self.view.data = {"recipes": page}

            self.view.template = "public/recipes/search/results"

        return self.view
