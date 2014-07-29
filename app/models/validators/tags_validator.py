#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


class TagsValidator(object):
    _tags_field = ""

    @staticmethod
    def parse_tags(tags):
        if isinstance(tags, str):
            tags = tags.split(",")
        new_tags = [ tag.lstrip().rstrip().lower() for tag in tags ]
        return new_tags

    @property
    def tags(self):
        return self._data.get(self._tags_field)

    @tags.setter
    def tags(self, val):
        tag = TagsValidator.parse_tags(val)
        self._data[self._tags_field] = tag
