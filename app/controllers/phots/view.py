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


@autoRoute()
class view(HTMLObject):
    """
    view, and if admin modify, a single image
    """
    _title = "phot"
    _defaultTmpl = "public/gifs/view"
    def GET(self):
        """
        """
        f = []
        for top, folders, files in os.walk(c.general.dirs["gifs"]):
            f.extend(files)
            break

        if self.request.id in f:
            raw = self.request.id.rsplit(".", 1)
            name = raw[0].replace("_", " ")
            self.view.data = {"picture": self.request.id, "name": name}
            return self.view
        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "That image could not be found. Sorry :/"}
            return self.view
