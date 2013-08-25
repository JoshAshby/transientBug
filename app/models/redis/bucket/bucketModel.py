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
from models.rethink.user.userModel import User
import config.config as c
import models.utils.dbUtils as dbu
import models.redis.baseRedisCollection as bc
from config.standard import StandardConfig


class bucketPail(bc.baseRedisCollection):
    def preInitAppend(self, drip):
        if "users" in drip:
            userList = []
            for user in drip.users:
                userList.append(User(user))
            drip._userObjects = userList
        return drip

    @staticmethod
    def toggle(bucketID):
        current = dbu.toBoolean(c.general["redis"].get("bucket:%s:value"%bucketID))
        return c.general["redis"].set("bucket:%s:value"%bucketID, not current)


class cfgBuckets(StandardConfig):
    def __init__(self):
        keys = {}
        for key in c.general.redis.keys("bucket:*:value"):
            keys[key.split(":")[1]] = dbu.toBoolean(c.general.redis.get(key))

        self._data = keys
