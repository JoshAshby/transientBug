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
        perpage = self.request.getParam("perpage", 5)
        sort_dir = self.request.getParam("dir", "desc")

        page_dict = {
            "perpage": perpage,
            "sort": sort_dir
            }

        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break

        if sort_dir == "asc":
            f.sort(reverse=True)
        elif sort_dir == "desc":
            f.sort()

        if perpage != "all":
            page_dict["show"] = True
            page = self.request.getParam("page", 0)

            perpage = int(perpage)
            page = int(page)

            offset_start = (perpage * page)
            offset_end = offset_start + perpage

            page_dict["next"] = page + 1
            page_dict["prev"] = page - 1

            if page != 0:
                page_dict["hasPrev"] = True
            else:
                page_dict["hasPrev"] = False

            if len(f) > offset_end:
                page_dict["hasNext"] = True
            else:
                page_dict["hasNext"] = False

            f = f[offset_start:offset_end]

        self.view.data = {"pictures": f, "page": page_dict}
        return self.view.render()
