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
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from utils.paginate import Paginate

from searchers.notes import NoteSearcher


@route()
@template("public/notes/search/index", "Notes")
class search(MixedObject):
    @HTML
    def GET(self):
        search_term = self.request.get_param("s")

        if search_term:
            searcher = NoteSearcher()
            parts = {"disable": False, "public": True, "draft": False}

            ids = searcher.search(search_term, collection=True)
            if ids is not None:
                ids.filter(parts)
                ids.fetch()

                page = Paginate(ids, self.request, "created", sort_direction_default="asc")
                self.view.data = {"page": page}

            else:
                self.view.data = {"page": None}

            self.view.template = "public/notes/search/results"

        return self.view
