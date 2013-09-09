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

from utils.paginate import pager


@login(["root"])
@autoRoute()
class index(HTMLObject):
    """
    Returns base index page listing all screenshots
    """
    _title = "screenshots"
    _defaultTmpl = "public/screenshots/index"
    def GET(self):
        """
        """
        self.view.data = {"header": "Screenshots"}

        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")

        self.view.scripts = ["scrn"]

        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break

        f, page_dict = pager(f, perpage, page, sort_dir)

        self.view.data = {"pictures": f, "page": page_dict}
        return self.view
