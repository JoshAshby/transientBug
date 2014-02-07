import os
import logging
import whoosh

from whoosh.index import EmptyIndexError

logger = logging.getLogger("search")

base_path = ""


class BaseSearcher(object):
    def __init__(self, schema=None):
        if schema:
            self.set_schema(schema)

        self.get_index()

    def set_schema(self, schema):
        self._schema = schema

    def get_index(self):
        try:
            self.open_index()
        except (EmptyIndexError, OSError) as e:
            logger.exception(e)
            if self._schema is not None:
                self.create_index()
            else:
                raise Exception("No schema defined, and no index found.")

    def create_index(self):
        if not os.path.exists(base_path+self.name):
            os.makedirs(base_path+self.name)
        self.ix = whoosh.index.create_in(base_path+self.name, self._schema)

    def open_index(self):
        self.ix = whoosh.index.open_dir(base_path+self.name)

    def add(self, item):
        pass

    def add_multiple(self, items):
        pass

    def update(self, item):
        pass

    def delete(self, id):
        document = whoosh.query.Term("id", id)
        self.writer.delete_by_query(document)

    def save(self):
        self.writer.commit()

    @property
    def writer(self):
        if not hasattr(self, "_writer") or not self._writer:
            self._writer = whoosh.writing.AsyncWriter(self.ix)
            #self._writer = self.ix.writer()

        return self._writer

    def search(self, search, limit=None):
        ids = []
        with self.ix.searcher() as searcher:
            if not isinstance(search, whoosh.qparser.QueryParser()):
                query = whoosh.qparser.QueryParser("content", self.ix.schema).parse(search)
            else:
                query = search
            results = searcher.search(query, limit=limit)

            for item in results:
                ids.append(item["id"])

            return ids

    def count(self):
        return self.ix.doc_count()

    def __len__(self):
        return self.count()
