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
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

import models.rethink.phot.photModel as pm
import rethinkdb as r


@login(["phots"])
@autoRoute()
class update(HTMLObject):
    """
    allows for the renaming of an image
    """
    _title = "rename phot"
    _defaultTmpl = "public/gifs/error"
    def POST(self):
        new_name = self.request.getParam("name")
        tags = self.request.getParam("tags")

        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_") for bit in tags.split(",") ]
        else:
            tag = []

        f = list(r.table(pm.Phot.table).filter({"filename": self.request.id}).run())
        if len(f):
            photo = pm.Phot(**f[0])
            photo.tags = tag

            self._redirect("/phots/view/%s" % photo.filename)

            if new_name != photo.title:
                new_name = new_name.replace(" ", "_")

                current_path = ''.join([c.general.dirs["gifs"], self.request.id])

                extension = self.request.id.rsplit(".", 1)[1]
                new_filename = ''.join([new_name, ".", extension])

                photo.filename = new_filename
                photo.title = self.request.getParam("name")

                new_name_path = ''.join([c.general.dirs["gifs"], new_filename])
                os.rename(current_path, new_name_path)

                loc = ''.join(["/phots/view/", new_name, ".", extension])
                self._redirect(loc)

            photo.save()

        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "That image could not be found. Sorry :/"}
            return self.view
