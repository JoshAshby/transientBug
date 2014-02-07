import search.base_search as searcher
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
from whoosh.analysis import FancyAnalyzer


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
        self.writer.add_document(

        )
