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
from utils.paginate import Paginate

import rethinkdb as r
import models.rethink.phot.photModel as pm

from fuzzywuzzy import fuzz


@autoRoute()
class tags(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "phots"
    _defaultTmpl = "public/gifs/index"
    def GET(self):
        """
        HOLY HELL WHAT A MESS
        """
        tag = self.request.id
        query = self.request.getParam("q")

        if not query and tag: query = tag

        if query:
            tags = list(r.table(pm.Phot.table).concat_map(lambda doc: doc["tags"]).run())
            new_tags = {}
            for t in tags:
                match = fuzz.partial_ratio(query, t.replace("_", " "))
                if match >= 85:
                    new_tags[t] = match

            tags = new_tags.copy().keys()
            if not tag:
                tag = max(new_tags, key=new_tags.get)

            self.view.data = {"q": query}

            orig_filt = self.request.getParam("filter", "all")
            view = self.request.getParam("v", 'cards').lower()

            if orig_filt == "all":
                filt = ""
            else:
                filt = orig_filt

            query = r.table(pm.Phot.table)

            if orig_filt != "all":
                query = query.filter({"extension": filt})

            query = query.filter(r.row["tags"].filter(lambda t: t == tag ).count() > 0)

            page = Paginate(query, self.request, "title")
            f = page.pail

            if f:
                new_f = []
                for bit in f:
                    phot = pm.Phot.fromRawEntry(**bit)
                    phot.format()
                    new_f.append(phot)
                f = new_f
            else:
                f = []

            self.view.data = {"pictures": f,
                              "tags": tags,
                              "tag": tag,
                              "pager": page,
                              "filter": orig_filt,
                              "v": view}
            return self.view

            #else:
                #self.view.template = "public/gifs/error"
                #self.view.data = {"error": "We do not currently have any photos in the tag: %s" % tag}
                #return self.view

        else:
            tags = list(r.table(pm.Phot.table).concat_map(lambda doc: doc["tags"]).run())

            if not tags:
                self.view.template = "public/gifs/error"
                self.view.data = {"error": "We do not currently have any tags within the system!"}
                return self.view

            tags = list(set(tags))
            tags.sort()

            self.view.template = "public/common/tags"
            self.view.data = {"tags": tags, "nav": {"phots": True}, "type": "Phots"}
            return self.view
