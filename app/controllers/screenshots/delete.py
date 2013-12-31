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

from seshat.route import autoRoute
from seshat.MixedObject import MixedObject
from seshat.objectMods import login
from seshat.funcMods import JSON
from seshat.actions import NotFound


@autoRoute()
@login(["root"])
class delete(MixedObject):
    @JSON
    def POST(self):
        current_path = ''.join([c.dirs.screenshots, self.request.id])

        f = []
        for top, folders, files in os.walk(c.dirs.screenshots):
            f.extend(files)
            break

        if self.request.id in f:
            os.remove(current_path)

            self.request.session.push_alert("Deleting screenshot...")
            return {"success": True}

        else:
            return NotFound()
