#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r
from rethinkORM import RethinkCollection

from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML, JSON

from utils.paginate import Paginate

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
@login(["admin"])
@template("admin/phots/index", "Phots")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "phots"})
        what = self.request.id
        orig = self.request.get_param("filter", "all")
        filt = dbu.phot_filter(orig)

        hidden_ids = list(r.table(pm.Phot.table).filter(r.row["disable"].eq(True)).concat_map(lambda doc: [doc["id"]]).run())

        if what == "enabled":
            query = r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"]))

        else:
            query = r.table(pm.Phot.table).filter(lambda doc: r.expr(hidden_ids).contains(doc["id"]))

        query = query.filter(lambda doc: doc["filename"].match(filt))

        result = RethinkCollection(pm.Phot, query=query)
        page = Paginate(result, self.request, "filename")


        self.view.data = {"page": page}
        self.view.scripts = ["transientbug/admin/phot"]

        return self.view

    @JSON
    def POST(self):
        current = pm.Phot(self.request.id)

        if current.filename:
            current.disable = not current.disable if "disable" in current._data else True
            current.save()

            return {"success": True}

        else:
            return {"success": False, "error": "That image couldn't be found. :/"}
