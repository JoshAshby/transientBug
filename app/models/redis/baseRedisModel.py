#!/usr/bin/env python
"""
fla.gr base model with a few classmethods and such to help
    keep a general interface across all models


http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c
import models.utils.dbUtils as dbu


class redisKeysBase(object):
    """
    Acts as the backing container for redisObject which will update the
    redis keys as the containers values and keys change.

    This could probably be tied into redisObject but then the code would
    get a little messy, I think so I'm keeping this separate. 
    """
    def __init__(self, key, redis=c.general["redis"]):
        self._data = dict()
        self.redis = redis
        self.key = key+":"

    def getField(self, key):
        objectType = self.redis.type(self.key+key)
        if objectType == "string":
            # If it's a string then we have to check if it
            # is a boolean or a regular string since
            # Redis doesn't have a concept of boolean it seems
            objectData = self.redis.get(self.key+key)
            try:
                objectData = dbu.toBoolean(objectData)
            except:
                pass
            self._data[key] = objectData
        if objectType == "list":
            self._data[key] = redisList(self.key+key)

    def __repr__(self):
        return str(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, item, value):
        if type(value) == list:
            self._data[item] = redisList(self.key+item, value)
        else:
            if value == None:
              value = ""
            self._data[item] = value
            self.redis.set(self.key+item, value)

    def __delitem__(self, item):
        del(self._data[item])
        self.redis.delete(self.key+item)

    def __contains__(self, item):
        if item in self._data:
            return True
        return False


class redisObject(object):
    """
    I said I never would, but this is another attempt at making
    an ORM for Redis...

    Emulates a python object and stores it in Redis real time.
    """
    protectedItems = ["_keys", "key", "redis", "id", "_finishInit"]
    def __init__(self, key, redis=c.general["redis"], **kwargs):
        self._keys = redisKeysBase(key, redis)
        self.redis = redis
        self.key = key
        self.id = self.key.split(":")[1]
        if not kwargs:
            bits = self.redis.keys("%s:*"%(key))
            for bit in bits:
                objectPart = bit.split("%s:"%(key))[1]
                self._keys.getField(objectPart)
        self._finishInit()

    def _finishInit(self):
      pass

    def _get(self, item):
        if item not in object.__getattribute__(self, "protectedItems") \
                and item[0] != "_":
            keys = object.__getattribute__(self, "_keys")
            if item in keys:
                return keys[item]
        return object.__getattribute__(self, item)

    def _set(self, item, value):
        if item not in object.__getattribute__(self, "protectedItems") \
                and item[0] != "_":
            keys = object.__getattribute__(self, "_keys")
            if not hasattr(value, '__call__'):
                keys[item] = value
                return value
            if hasattr(value, '__call__') and item in keys:
                raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __getattr__(self, item):
        return self._get(item)

    def __getitem__(self, item):
        return self._get(item)

    def __setattr__(self, item, value):
        return self._set(item, value)

    def __setitem__(self, item, value):
        return self._set(item, value)

    def __delitem__(self, item):
        keys = object.__getattribute__(self, "_keys")
        if item in keys:
            del(keys[item])
        else:
            object.__delitem__(self, item)

    def __contains__(self, item):
        keys = object.__getattribute__(self, "_keys")
        if item in keys:
            return True
        return False


class redisList(object):
    """
    Attempts to emulate a python list, while storing the list
    in Redis.

    Missing the sort and reverse functions currently
    """
    def __init__(self, key, start=[], redis=c.general["redis"], reset=False):
        self._list = []
        self.redis = redis
        self.key = key
        self.sync()
        if start and not reset:
            self.extend(start)
        if start and reset:
            self.reset()
            self.extend(start)

    def __repr__(self):
        return repr(self._list)

    def __str__(self):
        return str(self._list)

    def sync(self):
        self._list = self.redis.lrange(self.key, 0, -1)
        self.listToInt()

    def listToInt(self):
        for elem in range(len(self._list)):
            try:
                self._list[elem] = int(self._list[elem])
            except:
                pass

    def append(self, other):
        assert type(other) == list
        self._list.append(other)
        for key in other:
            self.redis.rpush(self.key, key) # because live fucks this up
        return self._list

    def extend(self, other):
        assert type(other) == list
        self._list.extend(other)
        for key in other:
            self.redis.rpush(self.key, key) # because live fucks this up
        return self._list

    def insert(self, index, elem):
        self._list.insert(index, elem)
        self.redis.linsert(self.key, 'AFTER', index, elem)
        return self._list

    def remove(self, elem):
        self._list.remove(elem)
        self.redis.lrem(self.key, 1, elem)
        return self._list

    def pop(self):
        value = self._list.pop()
        self.redis.lpop(self.key)
        return value

    def index(self, elem):
        return self._list.index(elem)

    def count(self):
        return self._list.count()

    def reset(self):
        self._list = []
        self.redis.delete(self.key)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value
        self.redis.lset(self.key, index, value)

    def __iter__(self):
        for item in self._list:
            yield item

    def __contains__(self, item):
        if item in self._list:
            return True
        return False
