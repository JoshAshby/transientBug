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
from seshat.actions import Redirect
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template, login
from seshat_addons.seshat.func_mods import HTML

from utils.paginate import Paginate

import rethinkdb as r
import models.rethink.recipe.recipeModel as rm
from searchers.recipes import RecipeSearcher

import whoosh.query as q


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
            if "recipe:" in search_term:
                parts = search_term.split(" ")
                for part in parts:
                    if "recipe:" in part:
                        recipe = rm.Recipe.find(part[7:])

                        if recipe is not None:
                            return Redirect("/recipes/{}".format(part[7:]))

            search_term = search_term.replace("tag:", "tags:")

            searcher = RecipeSearcher()

            if self.request.session.id:
                allow = q.Or([q.Term("user", self.request.session.id),
                              q.And([q.Term("public", True),
                                   q.Term("deleted", False),
                                   q.Term("reported", False)])
                              ])
            else:
                allow = q.And([q.Term("public", True),
                        q.Term("deleted", False),
                        q.Term("reported", False)])


            ids = searcher.search(search_term, collection=True, allow=allow)
            if ids is not None:
                ids.fetch()

                page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                self.view.data = {"recipes": page}

            self.view.template = "public/recipes/search/results"

        return self.view
