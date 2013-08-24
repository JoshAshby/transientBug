#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

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
from seshat.objectMods import login


@login()
@autoRoute()
class index(HTMLObject):
    """
    Returns base index page listing all screenshots
    """
    _title = "phots"
    _defaultTmpl = "public/screenshots/index"
    def GET(self):
        """
        """
        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break
        self.view.data = {"pictures": f}
        return self.view.render()
