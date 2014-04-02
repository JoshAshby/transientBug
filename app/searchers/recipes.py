#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import searchers.base_searcher as searcher

from whoosh.fields import SchemaClass, TEXT, ID, DATETIME, BOOLEAN
from whoosh.analysis import *
import models.rethink.recipe.recipeModel as rm


iwf_i = IntraWordFilter(mergewords=True, mergenums=True)
iwf_q = IntraWordFilter(mergewords=False, mergenums=False)
iwf = MultiFilter(index=iwf_i, query=iwf_q)

custom_analyzer = SpaceSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()
tag_analyzer = CommaSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()


class RecipeSchema(SchemaClass):
    id = ID(stored=True, unique=True)
    created = DATETIME()
    title = TEXT(analyzer=custom_analyzer)
    description = TEXT(analyzer=custom_analyzer)
    public = BOOLEAN()
    deleted = BOOLEAN()
    reported = BOOLEAN()
    short_code = ID(stored=True, unique=True)
    tags = TEXT(analyzer=tag_analyzer)
    user = ID()
    steps = TEXT(analyzer=custom_analyzer)
    ingredients = TEXT(analyzer=custom_analyzer)
    country = TEXT()


def get_recipe_data(recipe):
    d = {"id":unicode(recipe.id),
         "created":recipe.created.datetime,
         "title":unicode(recipe.title),
         "description":unicode(recipe.raw_description),
         "short_code":unicode(recipe.short_code),
         "user":unicode(recipe.user.id),
         "country": unicode(recipe.country),
         "deleted": recipe.deleted,
         "reported": recipe.reported,
         "public": recipe.public}

    if recipe.steps:
        d["steps"] = unicode(",".join(recipe.steps))

    if recipe.ingredients:
        d["ingredients"] = unicode(",".join(recipe.ingredients))

    if recipe.tags:
        d["tags"] = unicode(",".join(recipe.tags))

    return d


class RecipeSearcher(searcher.RethinkSearcher):
    name = "recipes"
    _schema = RecipeSchema
    _model = rm.Recipe
    _fields_to_search = ["title",
                         "short_code",
                         "description",
                         "tags",
                         "country",
                         "steps",
                         "ingredients",
                         "user"]

    def add(self, recipe):
        d = get_recipe_data(recipe)

        self.writer.add_document(**d)

        return self

    def update(self, recipe):
        d = get_recipe_data(recipe)

        self.writer.update_document(**d)

        return self
