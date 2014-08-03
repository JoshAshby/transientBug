#!/usr/bin/env python
"""Reindex

Util to reindex the various search indexes

Usage:
    reindex.py (<models>...) [-v | --verbose] [-d | --debug]
    reindex.py --version
    reindex.py (-h | --help)

Options:
    --help -h          Show this
    --debug -d         Start the service in debug mode
    --verbose -v       Log to the console along with default files
"""
import logging
import math
import rethinkdb as r
from docopt import docopt

import config.config as c

from searchers.phots import PhotSearcher
from searchers.notes import NoteSearcher
from searchers.recipes import RecipeSearcher

from rethinkORM import RethinkCollection

from models.rethink.phot.photModel import Phot
from models.rethink.note.noteModel import Note
from models.rethink.recipe.recipeModel import Recipe


logger = logging.getLogger(c.general.logName+".reindex")


class Batcher(object):
    batches = 25

    def __init__(self, model):
        self.model = model
        logger.debug("Setup model {}".format(self.model))

    def get_total_of_ids(self):
        total = r.table(self.model.table)\
          .count()\
          .run()

        logger.info("Total documents in table {}: {}".format(self.model.table, total))

        return total

    def get_batch(self, offset):
        documents = r.table(self.model.table)\
          .order_by(index='id')\
          .skip(offset)\
          .limit(self.batches)\
          .coerce_to('array')\
          .run()

        logger.debug("Batch for offset {}, limit {}: {}".format(offset, self.batches, documents))

        return documents

    def start_batching(self):
        number_of_runs = int(math.ceil(self.get_total_of_ids()/self.batches))

        logger.info("Doing a total of {} batchs".format(number_of_runs))

        for num in range(0, number_of_runs+1):
            logger.debug("Running batch #{}".format(num))
            skip = self.batches * num
            logger.debug("Skipping {} documents".format(skip))
            self.batch = self.get_batch(skip)
            logger.debug("Running next batch...")
            self.process_batch()
            logger.debug("Batch complete, moving on...")

        logger.debug("Batching complete, cleaning up...")
        self.cleanup()

    def process_batch(self):
        for doc in self.batch:
            self.get_model(doc)
            logger.debug("Processing model: {}".format(self.current))
            self.process_model()
            logger.debug("Model processed...")
            self.save_model()
            logger.debug("Model saved, moving on...")

    def get_model(self, doc):
        self.current = self.model(**doc)

    def process_model(self):
        pass

    def cleanup(self):
        pass

    def save_model(self):
        self.current.save()


class Indexer(Batcher):
    def __init__(self, model, Index):
        super(Indexer, self).__init__(model)

        self.indexer = Index()

    def process_model(self):
        self.indexer.update(self.current)

    def cleanup(self):
        self.indexer.save()


def reindex_phots():
    indexer = Indexer(Phot, PhotSearcher)
    indexer.start_batching()

def reindex_notes():
    indexer = Indexer(Note, NoteSearcher)
    indexer.start_batching()

def reindex_recipes():
    indexer = Indexer(Recipe, RecipeSearcher)
    indexer.start_batching()


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug v2.0.0')

    c.debug = True if arguments["--debug"] else False

    level = logging.INFO
    if c.debug:
        level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger()
    logger.setLevel(level)

    fh = logging.FileHandler(c.files.log)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if arguments["--verbose"]:
        try:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        except:
            pass

    if 'phots' in arguments['<models>']:
        reindex_phots()

    if 'notes' in arguments['<models>']:
        reindex_notes()

    if 'recipes' in arguments['<models>']:
        reindex_recipes()
