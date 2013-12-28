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
from seshat.MixedObject import MixedObject
from seshat.objectMods import login
from seshat.actions import Redirect

import rethinkdb as r
import models.rethink.phot.photModel as pm

import arrow


@login(["phots"])
@autoRoute()
class phot(MixedObject):
    _title = "new phots"
    _default_tmpl = "public/new/phot"
    def GET(self):
        return self.view.render()

    def POST(self):
        stuff = self.request.getParam("url", None) or self.request.getFile("file")
        title = self.request.getParam("title", "")
        tags = self.request.getParam("tags", "")

        if tags:
            if type(tags) is str:
                tag = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in tags.split(",") ]
            else:
                tag = tags
        else:
            tag = []

        found = r.table(pm.Phot.table).filter({"filename": title}).count().run()
        if found:
          title = "_".join([title, str(arrow.utcnow().timestamp)])
          self.request.session.push_alert("That image name is already in use; timestamp appened to image name.")

        phot = pm.Phot.new_phot(self.request.session.id,
                                stuff=stuff,
                                title=title,
                                tags=tag)

        self.request.session.push_alert("Image is being downloaded...")
        return Redirect("/phots/%s" % phot.short_code)
