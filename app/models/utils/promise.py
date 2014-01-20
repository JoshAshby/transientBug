"""
Make promises that something will happen by placing things in queues
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c


def redis_promise_provider(key, data):
    key = ":".join([key, "queue"])
    c.redis.rpush(key, data)


def id_promise(key):
    def cls_wrapper(cls):
        def wrapper(*args, **kwargs):
            res = cls(*args, **kwargs)

            redis_promise_provider(key, res.id)

            return res
        return wrapper
    return cls_wrapper
