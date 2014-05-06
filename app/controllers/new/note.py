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
import config.config as c
from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect

import models.rethink.note.noteModel as nm
from searchers.notes import NoteSearcher


@route()
@login(["notes"])
@template("public/new/note", "New Note")
class note(MixedObject):
    @HTML
    def GET(self):
        self.view.data = {"themes": c.general.slideshow_themes}
        return self.view

    def POST(self):
        title = self.request.get_param("title")
        contents = self.request.get_param("contents")
        public = self.request.get_param("public", False)
        draft = self.request.get_param("draft", False)
        toc = self.request.get_param("toc", False)
        comments = self.request.get_param("comments", False)
        tags = self.request.get_param("tags")
        theme = self.request.get_param("theme")

        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in tags.split(",") ]
        else:
            tag = []

        try:
            note = nm.Note.new_note(user=self.session.id,
                                    title=title,
                                    contents=contents,
                                    public=public,
                                    tags=tag,
                                    toc=toc,
                                    has_comments=comments,
                                    draft=draft,
                                    theme=theme)

            searcher = NoteSearcher()
            searcher.add(note)
            searcher.save()

        except Exception as e:
            print e
            self.session.push_alert("That note could not be created! %s" % e.message, level="error")
            return Redirect("/new/note")

        return Redirect("/notes/%s" % note.short_code)
