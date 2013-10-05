#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c
import arrow

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login
from seshat.actions import Redirect

from utils.paginate import Paginate
import utils.files as fu


@login(["root"])
@autoRoute()
class index(HTMLObject):
    _title = "screenshots"
    _defaultTmpl = "public/screenshots/index"
    def GET(self):
        """
        """
        self.view.data = {"header": "Screenshots"}
        self.view.scripts = ["scrn"]

        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break

        page = Paginate(f, self.request, sort_direction="asc")

        self.view.data = {"page": page}
        return self.view

    def POST(self):
        scrn = self.request.getFile("file")

        if scrn:
            date = str(arrow.utcnow().timestamp) + "_"

            path = ''.join([c.general.dirs["screenshots"], date, scrn.filename])
            try:
                fu.write_file(scrn, path)
                self.request.session.pushAlert("Screenshot uploaded...", level="success")
            except IOError as e:
                self.request.session.pushAlert("There was a problem executing that: {}".format(str(e)), level="error")

        return Redirect("/screenshots")
