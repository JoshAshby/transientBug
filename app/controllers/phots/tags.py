#!/usr/bin/env python
"""
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
from rethinkORM import RethinkCollection
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@autoRoute()
class tags(HTMLObject):
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        orig = self.request.getParam("filter", "all")
        filt = dbu.phot_filter(orig)
        tag = self.request.id or self.request.getParam("q")
        view = self.request.getParam("v", 'cards').lower()

        query = tag.replace("_", " ")

        hidden_ids = list(r.table(pm.Phot.table)\
            .filter(r.row["disable"].eq(True))\
            .concat_map(lambda doc: [doc["id"]]).run())

        base_query = r.table(pm.Phot.table)\
            .filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"]))\
            .filter(lambda doc: doc["filename"].match(filt))

        all_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        if query:
            try:
                similar, top = dbu.search_tags(all_tags, query)
            except Exception:
                self.view.template = "public/gifs/errors/no_matching_tags"
                self.view.data = {"tag": query}
                return self.view

            q = base_query.filter(r.row["tags"]\
                .filter(lambda t: t == top ).count() > 0)
            res = RethinkCollection(pm.Phot, query=q)
            page = Paginate(res, self.request, "title")

            self.view.data = {"tags": similar,
                              "tag": top,
                              "page": page,
                              "filter": orig,
                              "v": view,
                              "q": query}
            return self.view

        else:
            if not all_tags:
                self.view.template = "public/gifs/errors/no_tags"
                return self.view

            self.view.template = "public/common/tags"
            self.view.data = {"tags": all_tags,
                              "nav": {"phots": True},
                              "type": "Phots",
                              "where": "phots"}
            return self.view
