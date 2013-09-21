#!/usr/bin/env python
"""
generate various style of short codes

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import string
import random


def rand_short_code():
  chars = string.ascii_uppercase + string.digits
  return ''.join(random.choice(chars) for x in range(10))
