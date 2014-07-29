"""Mass Updater

Given a model and a migration function which operates on the model,
run it on every document within the models table.


Example:

>>> from utils.mass_updater import MassUpdater
>>> from migrations.phots_set_disabled import migration
>>> from models.rethink.phot.photModel import Phot
>>> mu = MassUpdater(Phot, migration)
>>> mu.start_migration()
"""
import logging
import math
import rethinkdb as r

import config.config as c

logger = logging.getLogger(c.general.logName+".mass_updater")


class MassUpdater(object):
    batches = 25

    def __init__(self, model, migration):
        self.model = model
        self.migration = migration
        logger.debug("Setup model {} and migration function {}".format(self.model, self.migration))

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

    def start_migration(self):
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

    def process_batch(self):
        for doc in self.batch:
            logger.debug("Processing document: {}".format(doc))
            self.get_model(doc)
            logger.debug("Now running migration function on model: {}".format(self.current))
            self.process_model()
            logger.debug("Migration done, saving model: {}".format(self.current))
            self.save_model()
            logger.debug("Model saved, moving on...")

    def get_model(self, doc):
        self.current = self.model(**doc)

    def process_model(self):
        self.migration(self.current)

    def save_model(self):
        self.current.save()
