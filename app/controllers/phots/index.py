#!/usr/bin/env python
"""
main index listing for gifs

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from utils.paginate import Paginate

import rethinkdb as r
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@autoRoute()
class index(HTMLObject):
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        orig = self.request.getParam("filter", "all")
        filt = dbu.phot_filter(orig)
        view = self.request.getParam("v", 'cards')

        """
        The SQL ~equ to what I'm aiming for
        SELECT * FROM phots WHERE id NOT IN ( SELECT * FROM phots WHERE disable == TRUE )
        """
        hidden_ids = list(r.table(pm.Phot.table).filter(r.row["disable"].eq(True)).concat_map(lambda doc: [doc["id"]]).run())

        query = r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"])).filter(lambda doc: doc["filename"].match(filt))

        page = Paginate(query, self.request, "title")
        f = page.pail

        if f:
            new_f = []
            for bit in f:
                phot = pm.Phot(**bit)
                phot.format()
                new_f.append(phot)

            self.view.data = {"pictures": new_f,
                              "filter": orig,
                              "v": view,
                              "pager": page}
            return self.view

        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "We do not currently have any photos that fit what you're looking for."}
            return self.view
