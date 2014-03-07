#!/usr/bin/env python
"""
Search all the notes!

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

import searchers.base_searcher as searcher

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
from whoosh.analysis import *
import models.rethink.note.noteModel as nm


iwf_i = IntraWordFilter(mergewords=True, mergenums=True)
iwf_q = IntraWordFilter(mergewords=False, mergenums=False)
iwf = MultiFilter(index=iwf_i, query=iwf_q)

custom_analyzer = SpaceSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()
tag_analyzer = CommaSeparatedTokenizer() | iwf | LowercaseFilter() | StemFilter()


class NoteSchema(SchemaClass):
    id = ID(stored=True, unique=True)
    created = DATETIME()
    title = TEXT(analyzer=custom_analyzer, spelling=True)
    contents = TEXT(spelling=True)
    public = BOOLEAN()
    draft = BOOLEAN()
    short_code = ID(stored=True, unique=True)
    disable = BOOLEAN()
    reported = BOOLEAN()
    tags = TEXT(analyzer=tag_analyzer, spelling=True)
    user = ID()


def get_note_data(note):
    d = {"id":unicode(note.id),
         "created":note.created.datetime,
         "title":unicode(note.title),
         "contents":unicode(note.contents),
         "public":note.public,
         "draft":note.draft,
         "short_code":unicode(note.short_code),
         "disable":note.disable,
         "reported":note.reported,
         "user":unicode(note.user)}

    if note.tags:
        d["tags"] = u",".join(note.tags)

    return d


class NoteSearcher(searcher.RethinkSearcher):
    name = "notes"
    _schema = NoteSchema
    _model = nm.Note
    _fields_to_search = ["title", "short_code", "contents", "tags"]

    def add(self, note):
        d = get_note_data(note)

        self.writer.add_document(**d)

        return self

    def update(self, note):
        d = get_note_data(note)

        self.writer.update_document(**d)

        return self
