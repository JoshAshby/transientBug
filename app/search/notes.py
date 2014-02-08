import copy

import search.base_searcher as searcher

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
from whoosh.analysis import FancyAnalyzer
from whoosh.qparser import QueryParser, MultifieldParser

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm

fields_to_search = ["title", "short_code", "contents", "tags"]


class NoteSchema(SchemaClass):
    id = ID(stored=True, unique=True)
    created = DATETIME()
    title = TEXT(analyzer=FancyAnalyzer, spelling=True)
    contents = TEXT(spelling=True)
    public = BOOLEAN()
    draft = BOOLEAN()
    short_code = ID(stored=True, unique=True)
    disabled = BOOLEAN()
    reported = BOOLEAN()
    tags = KEYWORD(commas=True)


class NoteSearcher(searcher.BaseSearcher):
    name = "notes"
    _schema = NoteSchema()

    def add(self, note):
      # This isn't at all anything near best practice, but it's my own module
      # and code so I'm allowing myself to do this. I wouldn't recommend it
      # however for anyone else to do.
        d = copy.copy(note._data) # BAD BAD BAD BAD
        tags = d.pop("tags")
        d["tags"] = ",".join(tags)

        d.pop("disable")
        d.pop("reported")
        d.pop("draft")
        d.pop("table_of_contents")
        d.pop("public")
        d.pop("created")
        d.pop("theme")
        d.pop("has_comments")
        d.pop("user")

        self.writer.add_document(**d)

    def search(self, search, limit=None):
        """
        Returns a RethinkCollection containing all notes which matched the
        query contained in `search`
        """
        ids = []
        with self.ix.searcher() as searcher:
            if not isinstance(search, QueryParser()):
                query = MultifieldParser(fields_to_search, self.ix.schema).parse(search)
            else:
                query = search
            results = searcher.search(query, limit=limit)

            for item in results:
                ids.append(item["id"])

        query = r.table(nm.Note.table).get_all(*ids)
        results = RethinkCollection(nm.Note, query=query)

        return results
