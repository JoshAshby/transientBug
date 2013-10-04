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
import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu

from fuzzywuzzy import fuzz


@autoRoute()
class tags(HTMLObject):
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        """
        HOLY HELL WHAT A MESS
        """
        orig = self.request.getParam("filter", "all")
        filt = dbu.phot_filter(orig)
        tag = self.request.id
        query = self.request.getParam("q")

        if not query and tag: query = tag

        hidden_ids = list(r.table(pm.Phot.table).filter(r.row["disable"].eq(True)).concat_map(lambda doc: [doc["id"]]).run())

        if query:
            tags = list(r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"])).concat_map(lambda doc: doc["tags"]).filter(lambda doc: doc["filename"].match(filt)).run())
            new_tags = {}
            for t in tags:
                match = fuzz.partial_ratio(query, t.replace("_", " "))
                if match >= 85:
                    new_tags[t] = match

            tags = new_tags.copy().keys()
            if not tag:
                try:
                    tag = max(new_tags, key=new_tags.get)
                except ValueError:
                    self.view.template = "public/gifs/error"
                    self.view.data = {"error": "I couldn't find any matching tags!"}
                    return self.view

            self.view.data = {"q": query}

            orig = self.request.getParam("filter", "all")
            filt = dbu.phot_filter(orig)
            view = self.request.getParam("v", 'cards').lower()

            query = r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"])).filter(lambda doc: doc["filename"].match(filt))

            query = query.filter(r.row["tags"].filter(lambda t: t == tag ).count() > 0)

            page = Paginate(query, self.request, "title")
            f = page.pail

            if f:
                new_f = []
                for bit in f:
                    phot = pm.Phot(**bit)
                    phot.format()
                    new_f.append(phot)
                f = new_f
            else:
                f = []

            self.view.data = {"pictures": f,
                              "tags": tags,
                              "tag": tag,
                              "pager": page,
                              "filter": orig,
                              "v": view}
            return self.view


        else:
            tags = list(r.table(pm.Phot.table).filter(lambda doc: ~r.expr(hidden_ids).contains(doc["id"])).filter(lambda doc: doc["filename"].match(filt)).concat_map(lambda doc: doc["tags"]).run())

            if not tags:
                self.view.template = "public/gifs/error"
                self.view.data = {"error": "We do not currently have any tags within the system!"}
                return self.view

            tags = list(set(tags))
            tags.sort()

            self.view.template = "public/common/tags"
            self.view.data = {"tags": tags, "nav": {"phots": True}, "type": "Phots", "where": "phots"}
            return self.view
