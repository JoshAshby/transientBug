#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
from models.validators.user_validator import UserValidator
from models.validators.tags_validator import TagsValidator
from models.validators.created_validator import CreatedValidator

import utils.short_codes as sc


class Recipe(UserValidator, TagsValidator, CreatedValidator, BaseInterface):
    table = "recipes"

    _user_field = "user"
    _tags_field = "tags"
    _created_field = "created"

    @classmethod
    def new_recipe(cls, user, title="", description="", country="'Merica!", ingredients=None, steps=None, tags=None, has_comments=False, public=False):
        if not tags:
            tags = []

        if not ingredients:
            ingredients = []

        if not steps:
            steps = []

        what = cls(user=user,
                          created=arrow.utcnow().timestamp,
                          title=title.rstrip().lstrip(),
                          description=description,
                          country=country,
                          ingredients=ingredients,
                          steps=steps,
                          tags=TagsValidator.parse_tags(tags),
                          public=public,
                          has_comments=has_comments,
                          short_code=sc.generate_short_code(cls.table),
                          deleted=False,
                          reported=False)

        what.save()

        return what

    #@property
    #def steps(self):
        #vals = []
        #keys = sorted([ int(i) for i in self._data["steps"].iterkeys() ])
        #for key in keys:
            #vals.append(self._["data"][key])

        #return vals

    #@steps.setter
    #def steps(self, val):
        #assert type(val) is list
        #ss = {}
        #for i in range(len(val)):
            #ss[str(i)] = val[i]

        #self._data["steps"] = ss

    def copy(self, user):
        copy_data = self._data.copy().pop("id").pop("user")
        copy_data["short_code"] = sc.generate_short_code(self.table)
        copy_data["created"] = arrow.utcnow().timestamp
        copy_data["user"] = user.id

        copy = Recipe(**copy_data)

        return copy

    def __json__(self):
        d = self._data.copy()
        d.pop("id")
        d.pop("disable") if "disable" in d else None
        d["user"] = self.user.username
        d["source"] = d.pop("url") if "url" in d else ""
        return d
