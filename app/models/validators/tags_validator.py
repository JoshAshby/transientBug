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
        new_tags = [ tag.lstrip().rstrip().replace(" ", "_").lower() for tag in tags ]
        return new_tags

    @property
    def tags(self):
        return self._data.get(self._tags_field)

    @tags.setter
    def tags(self, val):
        tag = [ bit.lstrip().rstrip().lower().replace(" ", "_") for bit in val ]
        self._data[self._tags_field] = tag
