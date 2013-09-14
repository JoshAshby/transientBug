#!/usr/bin/env python
"""
bucket model

Basically what we have is a key value store in redis
of all the session ID's (store and retrieved via the cookie
from Seshat)

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c
import models.utils.dbUtils as dbu
from config.standard import StandardConfig


def toggle_bucket(bucketID):
    """
    Toggles the given bucket via `bucketID` to the inverse of its current value
    """
    current = dbu.toBoolean(c.general["redis"].get("bucket:%s:value"%bucketID))
    return c.general["redis"].set("bucket:%s:value"%bucketID, not current)


class cfgBuckets(StandardConfig):
    def __init__(self):
        keys = { key.split(":")[1]:dbu.toBoolean(c.general["redis"].get(key)) for key in c.general.redis.keys("bucket:*:value") }

        self._data = keys
