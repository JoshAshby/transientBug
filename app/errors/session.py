#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


class SessionError(Exception): pass


class UsernameError(SessionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class PasswordError(SessionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class DisableError(SessionError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
