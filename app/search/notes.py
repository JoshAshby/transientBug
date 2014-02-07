import search.base_search as searcher
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
from whoosh.analysis import FancyAnalyzer

import copy


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

    def add(self, note):
      # This isn't at all anything near best practice, but it's my own module
      # and code so I'm allowing myself to do this. I wouldn't recommend it
      # however for anyone else to do.
        d = copy.copy(note._data) # BAD BAD BAD BAD
        tags = d.pop("tags")
        d["tags"] = ",".join(tags)
        self.writer.add_document(**d)
