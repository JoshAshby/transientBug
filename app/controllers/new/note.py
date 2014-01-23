#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

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
from seshat.actions import Redirect

import models.rethink.note.noteModel as nm


@route()
@login(["notes"])
@template("public/new/note", "New Note")
class note(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("note_create", "partials/public/note_create")
        return self.view

    def POST(self):
        title = self.request.get_param("title")
        contents = self.request.get_param("contents")
        public = self.request.get_param("public", False)
        draft = self.request.get_param("draft", True)
        toc = self.request.get_param("toc", False)
        tags = self.request.get_param("tags")

        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in tags.split(",") ]
        else:
            tag = []

        try:
            note = nm.Note.new_note(user=self.request.session.id,
                                    title=title,
                                    contents=contents,
                                    public=public,
                                    tags=tag,
                                    toc=toc,
                                    draft=draft)

        except Exception as e:
            self.request.session.push_alert("That note could not be created! %s" % e.message, level="error")
            return Redirect("/new/note")

        return Redirect("/notes/%s" % note.short_code)
