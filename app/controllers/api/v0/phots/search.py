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
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.func_mods import JSON

from utils.paginate import Paginate

from searchers.phots import PhotSearcher

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
class search(MixedObject):
    @JSON
    def GET(self):
        search_term = self.request.get_param("s")
        if search_term:
            search_term = search_term.replace("tag:", "tags:")

            searcher = PhotSearcher()
            phots_hidden_filter = dbu.rql_where_not(pm.Phot.table, "disable", True, raw=True)
            ids = searcher.search(search_term, collection=True, pre_filter=phots_hidden_filter)

            if ids is not None:
                ids.fetch()

                page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                return page.for_json()

            return {"page": None, "pail": None}

        return {"error": "No search (s) term provided."}
