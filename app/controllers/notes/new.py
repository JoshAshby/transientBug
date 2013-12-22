#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.MixedObject import MixedObject
from seshat.objectMods import login
from seshat.actions import Redirect

import models.rethink.note.noteModel as nm


@login(["notes"])
@autoRoute()
class new(MixedObject):
    _title = "new note"
    _default_tmpl = "public/notes/edit"
    def GET(self):
        """
        """
        self.view.data = {"note": None}
        return self.view

    def POST(self):
        title = self.request.getParam("title")
        contents = self.request.getParam("contents")
        public = self.request.getParam("public", False)
        tags = self.request.getParam("tags")

        if tags:
            tag = [ bit.lstrip().rstrip() for bit in tags.split(",") ]
        else:
            tag = []

        try:
            note = nm.Note.new_note(user=self.request.session.userID,
                        title=title,
                        contents=contents,
                        public=public,
                        tags=tag)

        except Exception as e:
            self.request.session.pushAlert("That note could not be created! %s" % e.message, level="error")
            return Redirect("/notes/new")

        return Redirect("/notes/view/%s" % note.short_code)
