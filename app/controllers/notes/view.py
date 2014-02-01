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
from seshat.actions import NotFound, Unauthorized, Redirect
from seshat_addons.seshat.func_mods import HTML
from seshat_addons.seshat.obj_mods import template

import rethinkdb as r
import models.rethink.note.noteModel as nm
import re

import utils.markdown_utils as md


@route()
@template("public/notes/view", "Note")
class view(MixedObject):
    @HTML
    def GET(self):
        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to('array')\
            .run()

        view_type = self.request.get_param("v")

        if f:
            note = nm.Note(**f[0])

            if not note.public:
              if not self.request.session.id or\
                  self.request.session.id!=note.user:
                  self.request.session.push_alert("That note is not public and you do not have the rights to access it.",
                                                  level="error")
                  return Unauthorized()

            if not self.request.session.has_notes and note.disable:
                return NotFound()

            if note.reported:
                self.seshat_addons.view.template = "public/notes/reported"
                return self.view

            if note.draft:
                self.view.skeleton = "skeletons/header"
                self.view.data = {"header": """
                  <span style="text-align: center">
                    <h1 style="font-weight: 700">DRAFT</h1>
                  </span>
                    """}

            if view_type == "slideshow":
# Sick/(ill) little bit of code to break things apart for remark.js
# Mildly ugly, and probably slow, but needed since remark doesn't
# accept making a new slide on each new h1 :/
                slide_break = "</section>\n<section>\n# "
                self.view.template = "public/notes/slideshow"
                raw = note.contents
                body = re.sub(r'(^\#\s)', slide_break, raw, flags=re.M)
                body = re.sub(re.escape("</section>"), "", body, count=1)
                self.view.data = {"body": md.markdown_raw(note.contents)}
                return self.view

            self.view.data = {"note": note}

            return self.view

        else:
            return NotFound()

    @HTML
    def POST(self):
        title = self.request.get_param("title")
        contents = self.request.get_param("contents")
        public = self.request.get_param("public", False)
        draft = self.request.get_param("draft", False)
        toc = self.request.get_param("toc", False)
        comments = self.request.get_param("comments", False)
        tags = self.request.get_param("tags")

        tag = []
        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in tags.split(",") ]

        f = r.table(nm.Note.table)\
            .filter({"short_code": self.request.id})\
            .coerce_to("array")\
            .run()

        if f:
            note = nm.Note(f[0]["id"])
            if note.author.id != self.request.session.id:
                self.request.session.push_alert("You don't own that note, you can't edit it!",
                                                level="danger")
                return Unauthorized()

            if not self.request.session.has_notes and note.disable:
                return NotFound()

            if note.reported:
                self.seshat_addons.view.template = "public/notes/reported"
                return self.view

            note.title = title
            note.contents = contents
            note.public = public
            note.tags = tag
            note.table_of_contents = toc
            note.draft = draft
            note.has_comments = comments

            note.save()

            return Redirect("/notes/%s" % note.short_code)

        else:
            return NotFound()
