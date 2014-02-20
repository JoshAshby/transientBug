#!/usr/bin/env python
"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

import searchers.base_searcher as searcher

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
import models.rethink.phot.photModel as pm
from whoosh.analysis import *


iwf_i = IntraWordFilter(mergewords=True, mergenums=True)
iwf_q = IntraWordFilter(mergewords=False, mergenums=False)
iwf = MultiFilter(index=iwf_i, query=iwf_q)

custom_analyzer = SpaceSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()
tag_analyzer = CommaSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()


class PhotSchema(SchemaClass):
    id = ID(stored=True, unique=True)
    created = DATETIME()
    title = TEXT(analyzer=custom_analyzer, spelling=True)
    short_code = ID(stored=True, unique=True)
    disable = BOOLEAN()
    tags = TEXT(analyzer=tag_analyzer, spelling=True)
    user = ID()


def get_phot_data(phot):
    d = {"id":unicode(phot.id),
         "created":arrow.get(phot.created).datetime,
         "title":unicode(phot.title),
         "short_code":unicode(phot.short_code),
         "disable":phot.disable if hasattr(phot, "disable") else False,
         "user":unicode(phot.user)}

    if phot.tags:
        d["tags"] = u",".join(phot.tags)

    return d


class PhotSearcher(searcher.RethinkSearcher):
    name = "phots"
    _schema = PhotSchema
    _model = pm.Phot
    _fields_to_search = ["title", "short_code", "tags"]

    def add(self, phot):
        d = get_phot_data(phot)

        self.writer.add_document(**d)

        return self

    def update(self, phot):
        d = get_phot_data(phot)

        self.writer.update_document(**d)

        return self
