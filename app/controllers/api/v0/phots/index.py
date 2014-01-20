#!/usr/bin/env python
"""
main index listing for gifs

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""

from seshat.route import route
from seshat_addons.MixedObject import MixedObject
from utils.paginate import Paginate
from seshat_addons.funcMods import JSON

from rethinkORM import RethinkCollection
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
class index(MixedObject):
    @JSON
    def GET(self):
        orig = self.request.get_param("filter", "all")
        filt = dbu.phot_filter(orig)

        query = dbu.rql_where_not(pm.Phot.table, "disable", True)
        query = query.filter(lambda doc: doc["filename"].match(filt))
        res = RethinkCollection(pm.Phot, query=query)

        page = Paginate(res, self.request, "title")

        return page.for_json()
