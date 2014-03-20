#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

import rethinkdb as r
from models.rethink.base_interface import BaseInterface
from models.validators.user_validator import UserValidator
from models.validators.tags_validator import TagsValidator
from models.validators.created_validator import CreatedValidator

import utils.short_codes as sc
import utils.markdown_utils as md


class Recipe(UserValidator, TagsValidator, CreatedValidator, BaseInterface):
    table = "recipes"

    _user_field = "user"
    _tags_field = "tags"
    _created_field = "created"

    @classmethod
    def find(cls, key):
        if len(key) == 10:
            res = r.table(cls.table).filter({"short_code": key})\
                    .coerce_to("array").run()

        elif len(key) == 36:
            res = r.table(cls.table).get(key).coerce_to("array").run()

        else:
            res = None

        if res:
            return cls(**res[0])

        return None

    @classmethod
    def new_recipe(cls, user, title="", description="", country="'Merica!", ingredients=None, steps=None, tags=None, has_comments=False, public=False):
        if not tags:
            tags = []

        if not ingredients:
            ingredients = []

        if not steps:
            steps = []

        what = cls.create(user=user,
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

    @property
    def description(self):
        if not hasattr(self, "_formated_description"):
            self._formated_description = md.markdown(self._data["description"])

        return self._formated_description

    @description.setter
    def description(self, val):
        self._data["description"] = val

    @property
    def raw_description(self):
        return self._data["description"]

    @property
    def steps(self):
        return self._data["steps"]

    @steps.setter
    def steps(self, val):
        if isinstance(val, str):
            val = val.split(",")
        new_val = filter(None, [ v.lstrip().rstrip() for v in val ])

        self._data["steps"] = new_val

    @property
    def ingredients(self):
        return self._data["ingredients"]

    @ingredients.setter
    def ingredients(self, val):
        if isinstance(val, str):
            val = val.split(",")
        new_val = filter(None, [ v.lstrip().rstrip() for v in val ])

        self._data["ingredients"] = new_val

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
