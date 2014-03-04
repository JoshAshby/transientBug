#!/usr/bin/env python
"""
main index listing for gifs

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
from seshat_addons.seshat.func_mods import JSON

from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
import rethinkdb as r

@route()
class index(MixedObject):
    @JSON
    def GET(self):
        query = r.table(nm.Note.table).filter({"disable": False,
            "reported": False,
            "public": True,
            "draft": False})

        res = RethinkCollection(nm.Note, query=query)

        page = Paginate(res, self.request, "created", sort_direction_default="asc")

        return page
