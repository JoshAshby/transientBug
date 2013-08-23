#!/usr/bin/env python
"""
Util for logging in and out

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""


class usernameError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class passwordError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class banError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
