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
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from utils.paginate import rethink_pager

import rethinkdb as r
import models.rethink.phot.photModel as pm


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
        sort_dir = self.request.getParam("dir", "asc")
        orig_filt = self.request.getParam("filter", "all")
        view = self.request.getParam("v", 'cards').lower()

        if orig_filt == "all":
            filt = ""
        else:
            filt = orig_filt

        query = r.table(pm.Phot.table)

        if orig_filt != "all":
            query = query.filter({"extension": filt})

        f, pager_dict = rethink_pager(query, self.request, "title")

        if f:
            new_f = []
            for bit in f:
                phot = pm.Phot.fromRawEntry(**bit)
                phot.format()
                new_f.append(phot)

            self.view.data = {"pictures": new_f, "page": pager_dict, "filter": orig_filt, view: True, "v": view}
            return self.view

        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "We do not currently have any photos that fit what you're looking for."}
            return self.view
