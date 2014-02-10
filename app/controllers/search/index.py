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
from searchers.phots import PhotSearcher

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
@template("public/search/index", "Search")
class search(MixedObject):
    @HTML
    def GET(self):
        search_term = self.request.get_param("s")

        if search_term:
            self.view.template = "public/search/results"

          # Notes searching
            searcher = NoteSearcher()
            notes_parts = {"disable": False, "public": True, "draft": False}

            notes_ids = searcher.search(search_term, collection=True)
            if notes_ids is not None:
                notes_ids.filter(notes_parts)
                notes_ids.fetch()

                note_page = Paginate(notes_ids, self.request, "created", sort_direction_default="asc")
                self.view.data = {"note_page": note_page}

            else:
                self.view.data = {"note_page": None}


          # Phots searching
            searcher = PhotSearcher()
            phots_hidden_query = dbu.rql_where_not(pm.Phot.table, "disable", True)
            phots_ids = searcher.search(search_term, collection=True, pre_query=phots_hidden_query)
            if phots_ids is not None:
                phots_ids.fetch()

                phot_page = Paginate(phots_ids, self.request, "created", sort_direction_default="asc")
                self.view.data = {"phot_page": phot_page}

            else:
                self.view.data = {"phot_page": None}

        return self.view
