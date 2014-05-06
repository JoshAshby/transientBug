#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c
import arrow

from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect

from utils.paginate import Paginate


@route()
@login(["screenshots"])
@template("public/screenshots/index", "Screenshots")
class index(MixedObject):
    @HTML
    def GET(self):
        f = []
        for top, folders, files in os.walk(c.dirs.screenshots):
            f.extend(files)
            break

        page = Paginate(f, self.request, sort_direction_default="asc")

        self.view.data = {"page": page}
        return self.view

    def POST(self):
        scrn = self.request.get_file("file")

        if scrn:
            date = str(arrow.utcnow().timestamp) + "_"

            path = ''.join([c.dirs.screenshots, date, scrn.filename])
            try:
                with open(path, 'w+b') as f:
                    f.write(scrn.read())
                self.session.push_alert("Screenshot uploaded...", level="success")
            except IOError as e:
                self.session.push_alert("There was a problem executing that: {}".format(str(e)), level="error")

        return Redirect("/screenshots")
