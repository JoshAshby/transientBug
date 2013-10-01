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
from seshat.baseObject import JSONObject
from seshat.objectMods import login

import models.rethink.note.noteModel as nm

import rethinkdb as r

import arrow


@login(["notes"])
@autoRoute()
class update(JSONObject):
    def POST(self):
        title = self.request.getParam("title")
        contents = self.request.getParam("contents")
        public = self.request.getParam("public", False)
        tags = self.request.getParam("tags")

        if tags:
            tag = [ bit.lstrip().rstrip() for bit in tags.split(",") ]
        else:
            tag = []

        note = self.request.id

        f = r.table(nm.Note.table).filter({"short_code": note}).run()

        f = list(f)
        if f:
            f = f[0]

            time = arrow.utcnow().timestamp
            try:
                note = nm.Note(**f)

                note.user=self.request.session.userID
                note.title=title
                note.contents=contents
                note.public=public
                note.tags=tag
                note.created=time

                note.save()

                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}

        else:
            return {"success": False, "error": "That note couldn't be found. :/"}
