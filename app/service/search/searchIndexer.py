#!/usr/bin/env python
"""
fla.gr daemon piece for indexing things when certian messages come through zmq

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from gevent import monkey; monkey.patch_all()
import gevent

from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.connect("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "")

from whoosh.filedb.filestore import FileStorage

from whoosh.fields import *

import os

import models.couch.flag.flagModel as fm

import config.config as c

import logging
logger = logging.getLogger(c.general.logName+"search.indexer")


flagSchema = Schema(title=TEXT,
    id=ID(stored=True, unique=True),
    description=TEXT,
    labels=KEYWORD(commas=True),
    url=TEXT,
    created=DATETIME,
    userID=TEXT)

flagSearchIndex = "/.flagSearchIndex"

if not os.path.exists(c.general.baseFolder+flagSearchIndex):
    os.mkdir(c.general.baseFolder+flagSearchIndex)
    logger.debug("Made directory: "+c.general.baseFolder+flagSearchIndex)

storage = FileStorage(c.general.baseFolder+flagSearchIndex)


def buildIndexes():
    logger.debug("Making new index of flags...")
    ix = storage.create_index(flagSchema)

    writer = ix.writer()

    flags = fm.flagORM.all()
    flags = fm.formatFlags(flags, True)

    for flag in flags:
        logger.debug("Flag: " +flag.id+" Indexed")
        labels = ", ".join(flag.labels)

        writer.update_document(title=flag.title,
            id=flag.id,
            description=flag.description,
            labels=labels,
            url=flag.url,
            userID=flag.userID,
            created=flag.created)

    writer.commit()


def updateFlags():
    logger.debug("Rebuilding index of flags...")
    ix = storage.open_index()

    flags = list(fm.flagORM.view(c.database.couchServer, 'typeViews/flag'))
    flags = fm.formatFlags(flags, True)

    currentFlags = set()
    indexedFlags = set()

    with ix.searcher() as searcher:
        writer = ix.writer()

        for fields in searcher.all_stored_fields():
            if fields["id"] not in currentFlags:
                writer.delete_by_term('id', fields["id"])
            else:
                indexedFlags.add(fields["id"])

    for flag in flags:
        labels = ", ".join(flag.labels)

        writer.update_document(title=flag.title,
            id=unicode(flag.id),
            description=flag.description,
            labels=labels,
            url=flag.url,
            userID=flag.userID,
            created=flag.created)
        currentFlags.add(flag.id)

    writer.commit()


def updateIndex():
    count = 0
    while True:
        reply = zmqSock.recv()
        logger.debug("Got: "+reply)
        if reply == "flagIndexUpdate up":
            logger.debug("Got count, count is currently: "+str(count))
            count += 1
            if count >= 5:
                updateFlags()
                count = 0

            elif reply == "flagIndexUpdate now":
                logger.debug("Got manual, updating index.")
                updateFlags()
                count = 0
        logger.debug("Count is now: "+str(count))


def start():
    logger.debug("Starting up...")
    ser = gevent.spawn(updateIndex)
    try:
        ser.join()
    except Exception as exc:
        gevent.shutdown
        logger.debug("Got exception: " + exc)
    except KeyboardInterrupt:
        gevent.shutdown
    else:
        gevent.shutdown
