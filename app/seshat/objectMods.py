#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
modifying decorators

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""


def admin(level=50):
        def wrapper(HTTPObject):
            HTTPObject.__level__ = level
            HTTPObject.__admin__ = True
            return HTTPObject
        return wrapper


def login(allowBan=False):
    def wrapper(HTTPObject):
        HTTPObject.__login__ = True
        return HTTPObject
    return wrapper
