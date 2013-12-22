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
from seshat.actions import NotFound, Redirect, Unauthorized

import models.rethink.phot.photModel as pm
import rethinkdb as r


@autoRoute()
class view(MixedObject):
    _title = "phot"
    _default_tmpl = "public/phots/view"
    def GET(self):
        phot = self.request.id

        # check if its a short code by looking for an extension
        # otherwise we assume it's a filename
        if len(phot.rsplit(".")) >= 1:
            f = r.table(pm.Phot.table).filter({"short_code": phot})\
                .coerce_to("array").run()
        else:
            f = list(r.table(pm.Phot.table).filter({"filename": phot}).run())

        if not f:
            return NotFound()

        if "disable" in f[0] and f[0]["disable"] and \
                not self.request.session.has_phots:
            return NotFound()

        photo = pm.Phot(**f[0])

        self.view.data = {"phot": photo}

        # TODO: CLEAN (WITH FIRE)
        if self.request.session.has_phots:
            self.view.scripts = ["pillbox",
                                 "lib/typeahead.min",
                                 "transientbug/phot",
                                 "transientbug/admin/phot"]
            self.view.stylesheets = ["pillbox"]

        return self.view

    def POST(self):
        if not self.request.session.has_phots:
            return Unauthorized()

        new_name = self.request.getParam("name")
        tags = self.request.getParam("tags")

        if tags:
            tag = [ bit.lstrip().rstrip().replace(" ", "_") for bit in tags.split(",") ]
        else:
            tag = []

        f = list(r.table(pm.Phot.table).filter({"filename": self.request.id}).run())
        if f:
            photo = pm.Phot(**f[0])
            photo.tags = tag

            if new_name != photo.title:
                new_name = new_name.replace(" ", "_")

                current_path = ''.join([c.dirs.gifs, self.request.id])

                extension = self.request.id.rsplit(".", 1)[1]
                new_filename = ''.join([new_name, ".", extension])

                photo.filename = new_filename
                photo.title = self.request.getParam("name")

                new_name_path = ''.join([c.dirs.gifs, new_filename])
                os.rename(current_path, new_name_path)

                loc = ''.join(["/phots/view/", new_name, ".", extension])
                self._redirect(loc)

            photo.save()

            return Redirect("/phots/"+photo.short_code)

        else:
            return NotFound()
