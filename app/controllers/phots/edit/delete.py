#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login, admin


@admin()
@login()
@autoRoute()
class delete(HTMLObject):
    """
    allows for the renaming of an image
    """
    _title = "rename phot"
    _defaultTmpl = "public/gifs/error"
    def POST(self):
        current_path = ''.join([c.general.dirs["gifs"], self.request.id])

        f = []
        for top, folders, files in os.walk(c.general.dirs["gifs"]):
            f.extend(files)
            break

        if self.request.id in f:
            try:
                os.remove(current_path)

                self.head = ("303 SEE OTHER",
                    [("location", "/phots")])

            except Exception as e:
                self.view.data = {"error": "That image could not be renamed: %s" % e.msg}
                return self.view

        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "That image could not be found. Sorry :/"}
            return self.view
