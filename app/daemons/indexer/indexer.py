#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from daemons.worker import Worker

import config.config as c

import models.rethink.user.userModel as um
import models.rethink.note.noteModel as nm

import arrow
import logging

logger = logging.getLogger(c.indexer.log_name)


class Indexer(Worker):
    name = "indexer"
    def build(self):
        pass
