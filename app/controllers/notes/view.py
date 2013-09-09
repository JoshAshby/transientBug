#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

import rethinkdb as r
import models.rethink.note.noteModel as nm


#@login(["notes"])
@autoRoute()
class view(HTMLObject):
    """
    """
    _title = "note"
    _defaultTmpl = "public/notes/view"
    def GET(self):
        """
        """
        note = self.request.id

        f = r.table(nm.Note.table).filter({"short_code": note}).run()

        f = list(f)
        if f:
            f = f[0]

            note = nm.Note.fromRawEntry(**f)

            if not note.public:
                if not self.request.session.userID \
                      or not self.request.session.has_notes \
                      or self.request.session.userID!=note.user:
                    self.request.session.pushAlert("That note is not public and you do not have the rights to access it.", level="error")
                    self._redirect("/notes")
                    return

            is_author = False
            if note.user == self.request.session.userID:
                is_author = True

            note.format()

            if self.request.session.has_notes:
                self.view.scripts = ["note"]

            if note.public:
                title = """<i class="icon-eye-open"></i> """
            else:
                title = """<i class="icon-eye-close"></i> """

            title += note.title

            self.view.data = {"note": note, "header": title, "is_author": is_author}
            return self.view
        else:
            self.request.session.pushAlert("That note could not be found!", level="error")
            self._redirect("/notes")
            return
