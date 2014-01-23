#!/usr/bin/env python
"""
Generate various style of short codes

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import string
import random
import rethinkdb as r


def rand_short_code(length=10):
    """
    Its simple: No, we don't kill the batman. We generate random code.
    Return a random selection of alphanumeric symbols. Not guaranteed to be
    unique in any case.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(length))


def generate_short_code(table):
    """
    Generates a new short_code, then checks to make sure it already isn't in
    the given table, and keeps going till it finds a unique code

    :param table: A `str` of the rethinkdb table to check for short_code
    collisions
    """
    code_good = False
    code = ""
    while not code_good:
        code = rand_short_code()
        f = r.table(table).filter({"short_code": code}).count().run()
        if f == 0:
            code_good = True

    return code
