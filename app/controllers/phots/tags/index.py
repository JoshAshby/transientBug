#!/usr/bin/env python
"""
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

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu

import utils.search as s


@route()
@template("public/phots/single_tag", "Phots")
class index(MixedObject):
    @HTML
    def GET(self):
        orig = self.request.get_param("filter", "all")
        filt = dbu.phot_filter(orig)
        query = self.request.id or self.request.get_param("q")

        q = dbu.rql_where_not(pm.Phot.table, "disable", True)
        q = q.filter(lambda doc: doc["filename"].match(filt))

        all_tags = q\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        if query:
            similar, top = s.search_tags(all_tags, query)

            top_other = top.replace("_", " ")
            top = top.replace(" ", "_")

            q = q.filter(r.row["tags"]\
                 .contains(lambda t: (t == top) | (t == top_other) ))

            res = RethinkCollection(pm.Phot, query=q)
            page = Paginate(res, self.request, "title")

            self.view.data = {"tags": similar,
                              "tag": top,
                              "page": page}
            return self.view

        else:
            self.seshat_addons.view.template = "public/phots/tags"

            self.view.data = {"tags": all_tags}

            return self.view
