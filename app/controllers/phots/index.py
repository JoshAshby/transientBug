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
from seshat.MixedObject import MixedObject
from utils.paginate import Paginate

from rethinkORM import RethinkCollection
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@autoRoute()
class index(MixedObject):
    _title = "phots"
    _default_tmpl = "public/gifs/index"
    def GET(self):
        orig = self.request.getParam("filter", "all")
        filt = dbu.phot_filter(orig)
        view = self.request.getParam("v", 'cards')

        query = dbu.rql_where_not(pm.Phot.table, "disable", True)
        query = query.filter(lambda doc: doc["filename"].match(filt))
        res = RethinkCollection(pm.Phot, query=query)

        page = Paginate(res, self.request, "title")

        self.view.data = {"filter": orig,
                          "v": view,
                          "page": page}

        return self.view
