#!/usr/bin/env python
"""
fla.gr helper utils for mainly the redis db models

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import string
import random


def short_code():
  chars = string.ascii_uppercase + string.digits
  return ''.join(random.choice(chars) for x in range(10))

def toBoolean(str):
    if str == 'True':
        return True
    elif str == 'False':
        return False
    else:
        raise Exception("Not a boolean")
