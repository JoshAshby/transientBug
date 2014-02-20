#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect

import rethinkdb as r
import models.rethink.phot.photModel as pm
from searchers.phots import PhotSearcher
import arrow


@route()
@login(["phots"])
@template("public/new/phot", "New Phot")
class phot(MixedObject):
    @HTML
    def GET(self):
        return self.view

    def POST(self):
        stuff = self.request.get_param("url", None) or self.request.get_file("file")
        title = self.request.get_param("title", "")
        tags = self.request.get_param("tags", "")

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

        searcher = PhotSearcher()
        searcher.update(phot)
        searcher.save()

        self.request.session.push_alert("Image is being downloaded...")
        return Redirect("/phots/%s" % phot.short_code)
