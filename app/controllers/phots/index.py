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
from utils.paginate import pager


@autoRoute()
class index(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        """
        """
        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")

        f = []
        for top, folders, files in os.walk(c.general.dirs["gifs"]):
            f.extend(files)
            break

        f, page_dict = pager(f, perpage, page, sort_dir)

        self.view.data = {"pictures": f, "page": page_dict}
        return self.view.render()
