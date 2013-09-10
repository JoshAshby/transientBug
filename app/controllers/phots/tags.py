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
class tags(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        """
        """
        tag = self.request.id

        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "asc")
        orig_filt = self.request.getParam("filter", "all")

        if orig_filt == "all":
            filt = ""
        else:
            filt = orig_filt

        query = r.table(pm.Phot.table)

        if orig_filt != "all":
            query = query.filter({"extension": filt})

        query = query.filter(r.row["tags"].filter(lambda t: t == tag).count() > 0)

        f, pager_dict = rethink_pager(query, perpage, page, sort_dir, "title")

        new_f = []
        for bit in f:
            phot = pm.Phot.fromRawEntry(**bit)
            phot.format()
            new_f.append(phot)

        self.view.data = {"pictures": new_f, "page": pager_dict, "filter": orig_filt, "tag": tag}
        return self.view
