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
from seshat_addons.mixed_object import MixedObject
from utils.paginate import Paginate
from seshat_addons.func_mods import JSON

from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
import models.utils.dbUtils as dbu


@route()
class index(MixedObject):
    @JSON
    def GET(self):
        query = dbu.rql_where_not(nm.Note.table, "disable", True)
        res = RethinkCollection(nm.Note, query=query)

        page = Paginate(res, self.request, "title")

        return page.for_json()
