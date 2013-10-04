#!/usr/bin/env python
"""
helper utils for mainly the redis db models

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com

"""

def toBoolean(str):
    if str == 'True':
        return True
    elif str == 'False':
        return False
    else:
        raise Exception("Not a boolean")

def phot_filter(filt):
    if filt == "all":
        orig = "$"
    if filt in ["gif", "png", "tiff"]:
        orig = filt+"$"
    if filt == "jpg":
        orig = "jp(eg|g)$"
    return orig
