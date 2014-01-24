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
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import login, template
from seshat_addons.func_mods import HTML

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm
from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/notes/index", "Notes")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar",
                          {"command": "notes"})

# I should figure out a way to do this filter stuff a little easier... hmm
        filter_parts = {}
        public = self.request.get_param("public")
        draft = self.request.get_param("draft")
        disabled = self.request.get_param("disable")
        reported = self.request.get_param("reported", False)
        sort_by = self.request.get_param("sort_by", "created")

        if not sort_by in ["created", "title", "public", "reported", "draft",
            "disable", "author.id"]:
            sort_by = "created"

            # should this be something I try to start doing? :/
            self.request.session.push_alert("Couldn't figure out what to sort by, as a result of an invalid value for sort_by.",
                                            level="error")

        if public:
            filter_parts["public"] = False if public == "private" else True
        if draft:
            filter_parts["draft"] = False if draft == "published" else True
        if disabled:
            filter_parts["disable"] = False if disabled == "enabled" else True

        filter_parts["reported"] = reported

        q = r.table(nm.Note.table).filter(filter_parts)

        res = RethinkCollection(nm.Note, query=q)
        page = Paginate(res, self.request, sort_by)

        self.view.data = {"page": page}

        return self.view
