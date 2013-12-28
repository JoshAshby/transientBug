#!/usr/bin/env python
"""
Utils for interacting with images.

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import tempfile
import shutil


class TemporaryDirectory(object):
    def __init__(self, suffix="", prefix="tmp_", dir=None):
        self.tmp = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)

    def __enter__(self):
        return self.tmp

    def __exit__(self, *errors):
        return self.destroy()

    def destroy(self):
        if self.tmp:
            shutil.rmtree(self.tmp)
        self.tmp = ""

    def __del__(self):
        if "tmp" in self.__dict__:
            self.__exit__(None, None, None)

    def __str__(self):
        if self.name:
            return "< TemporaryDirectory at: %s >" % (self.name)
        else:
            return "< Deleted TemporaryDirectory >"
