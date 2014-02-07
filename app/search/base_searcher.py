import os
import logging
import whoosh

from whoosh.index import EmptyIndexError

logger = logging.getLogger("search")


class BaseSearcher(object):
    def __init__(self, index_name, schema=None):
        self._name = index_name
        self._path = self._name
        self._schema = schema

        self.get_index()

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
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        self.ix = whoosh.index.create_in(self._path, self._schema)

    def open_index(self):
        self.ix = whoosh.index.open_dir(self._path)

    def add(self, item):
        writer = whoosh.writing.AsyncWriter(self.ix)
      # Fill in stuff to add
        writer.commit()

    def add_multiple(self, items):
        writer = whoosh.writing.AsyncWriter(self.ix)
      # Fill in stuff to add
        for item in items:
          # writer.add_document()
            pass

        writer.commit()

    def update(self, item):
        writer = whoosh.writing.AsyncWriter(self.ix)
      # writer.update_document()
      # Fill in stuff to add
        writer.commit()

    def delete(self, id):
        writer = self.ix.writer()
        document = whoosh.query.Term("id", id)
        writer.delete_by_query(document)
        writer.commit()

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
