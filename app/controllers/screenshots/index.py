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
from seshat.MixedObject import MixedObject
from seshat.objectMods import login
from seshat.actions import Redirect

from utils.paginate import Paginate


@login(["screenshots"])
@autoRoute()
class index(MixedObject):
    _title = "screenshots"
    _default_tmpl = "public/screenshots/index"
    def GET(self):
        """
        """
        f = []
        for top, folders, files in os.walk(c.dirs.screenshots):
            f.extend(files)
            break

        page = Paginate(f, self.request, sort_direction="asc")

        self.view.data = {"page": page}
        return self.view

    def POST(self):
        scrn = self.request.getFile("file")

        if scrn:
            date = str(arrow.utcnow().timestamp) + "_"

            path = ''.join([c.dirs.screenshots, date, scrn.filename])
            try:
                with open(path, 'w+b') as f:
                    f.write(scrn.read())
                self.request.session.push_alert("Screenshot uploaded...", level="success")
            except IOError as e:
                self.request.session.push_alert("There was a problem executing that: {}".format(str(e)), level="error")

        return Redirect("/screenshots")
