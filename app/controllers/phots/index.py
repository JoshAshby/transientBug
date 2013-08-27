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
        sort_dir = self.request.getParam("dir", "desc").lower()
        orig_filt = self.request.getParam("filter", "all").lower()

        f = []
        for top, folders, files in os.walk(c.general.dirs["gifs"]):
            f.extend(files)
            break

        new_f = []
        if orig_filt != "all":
            if orig_filt == "jpg":
                filt = ["jpg", "jpeg"]
            elif orig_filt == "non_gif":
                filt = ["jpg", "jpeg", "png", "tiff"]
            else:
                filt = [orig_filt]

            for img in f:
                bits = img.rsplit(".", 1)
                if len(bits) > 1:
                    if bits[1].lower() in filt:
                        new_f.append(img)

            f = new_f

        f, page_dict = pager(f, perpage, page, sort_dir)

        self.view.data = {"pictures": f, "page": page_dict, "filter": orig_filt}
        return self.view
