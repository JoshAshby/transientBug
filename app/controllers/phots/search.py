#!/usr/bin/env python
"""
main index listing for notes - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat.actions import Redirect
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from utils.short_codes import short_code_in_search
from utils.paginate import Paginate

import whoosh.query as q
from searchers.phots import PhotSearcher

import rethinkdb as r
import models.rethink.phot.photModel as pm


@route()
@template("public/phots/search/index", "Phots Search")
class search(MixedObject):
    @HTML
    def GET(self):
        view = self.request.get_param("v")

        all_tags = r.table(pm.Phot.table)\
            .filter({"disable": False})\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        if "phot_view" in self.session.data:
            if not view:
                view = self.session.data.phot_view
        else:
            self.session.data.phot_view = "cards"
            view = "cards"

        self.session.data.phot_view = view

        self.view.data = {
            "tags": all_tags,
            "phot_page": None
        }

        search_term = self.request.get_param("s")
        if search_term:
            short = short_code_in_search("phot", search_term)
            if short:
                return Redirect("/phots/{}".format(short))

            search_term = search_term.replace("tag:", "tags:")

            searcher = PhotSearcher()

            allow = q.And([
                q.Term("disable", False)
            ])

            ids = searcher.search(search_term, collection=True, allow=allow)

            if ids is not None:
                ids.fetch()

                page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                self.view.data = {"phot_page": page, "v": view}

            self.view.template = "public/phots/search/results"

        return self.view
