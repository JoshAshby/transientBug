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
from seshat_addons.seshat.func_mods import JSON

from utils.paginate import Paginate

from searchers.recipes import RecipeSearcher
import whoosh.query as q


@route()
class search(MixedObject):
    @JSON
    def GET(self):
        search_term = self.request.get_param("s")
        if not search_term:
            return {"recipes": None}

        else:
            search_term = search_term.replace("tag:", "tags:")

            searcher = RecipeSearcher()

            if self.request.session.id:
                allow = q.Or([q.Term("user", self.request.session.id),
                              q.And([q.Term("public", True),
                                   q.Term("deleted", False),
                                   q.Term("reported", False)])
                              ])
            else:
                allow = q.And([q.Term("public", True),
                        q.Term("deleted", False),
                        q.Term("reported", False)])

            ids = searcher.search(search_term, collection=True, allow=allow)

            if ids is not None:
                page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                return {"recipes": page}

        return {"recipes": None}
