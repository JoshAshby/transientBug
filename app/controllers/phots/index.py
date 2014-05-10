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
from seshat_addons.seshat.mixed_object import MixedObject
from utils.paginate import Paginate
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from rethinkORM import RethinkCollection
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
@template("public/phots/index", "Phots")
class index(MixedObject):
    @HTML
    def GET(self):
        orig = self.request.get_param("filter", "all")
        filt = dbu.phot_filter(orig)
        view = self.request.get_param("v")

        if "phot_view" in self.session.data:
            if not view:
                view = self.session.data.phot_view

        self.session.data.phot_view = view

        if not self.session.data.phot_view:
            self.session.data.phot_view = "cards"
            view = "cards"

        query = dbu.rql_where_not(pm.Phot.table, "disable", True)
        query = query.filter(lambda doc: doc["filename"].match(filt))

        res = RethinkCollection(pm.Phot, query=query)

        page = Paginate(res, self.request, "title")

        return {"filter": orig,
                "v": view,
                "phot_page": page}
