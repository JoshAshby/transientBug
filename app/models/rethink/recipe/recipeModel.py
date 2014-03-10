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


class Recipe(BaseInterface, UserValidator, TagsValidator, CreatedValidator):
    table = "recipes"

    _user_field = "user"
    _tags_field = "tags"
    _created_field = "created"

    @classmethod
    def new(cls, user, title="", tags=None, country="'Merica!", ingredients=None, steps=None, has_comments=False, public=False):
        if not tags:
            tags = []

        if not ingredients:
            ingredients = []

        if not steps:
            steps = []

        title = title.rstrip().lstrip().replace(" ", "_").lower()
        created = arrow.utcnow().timestamp

        new_tags = [ tag.lstrip().rstrip().replace(" ", "_").lower() for tag in tags ]

        code = sc.generate_short_code(cls.table)

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          public=public,
                          tags=new_tags,
                          has_comments=has_comments,
                          short_code=code,
                          disable=False,
                          reported=False)

        return what

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
