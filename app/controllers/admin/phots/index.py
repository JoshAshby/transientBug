#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r
from rethinkORM import RethinkCollection

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

from utils.paginate import Paginate

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@login(["admin"])
@autoRoute()
class index(HTMLObject):
    _title = "Buckets"
    _defaultTmpl = "admin/phots/index"
    def GET(self):
        what = self.request.id
        orig = self.request.getParam("filter", "all")
        filt = dbu.phot_filter(orig)

        hidden_ids = list(r.table(pm.Phot.table).filter(r.row["disable"].eq(True)).concat_map(lambda doc: [doc["id"]]).run())

        if what == "enabled":
            query = r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"]))

        else:
            query = r.table(pm.Phot.table).filter(lambda doc: r.expr(hidden_ids).contains(doc["id"]))

        query = query.filter(lambda doc: doc["filename"].match(filt))

        result = RethinkCollection(pm.Phot, query=query)
        page = Paginate(result, self.request, "filename")


        self.view.data = {"page": page, "what": what, "filter": orig}
        self.view.scripts = ["admin/phot"]

        return self.view
