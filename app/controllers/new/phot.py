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

import models.rethink.phot.photModel as pm


@login(["phots"])
@autoRoute()
class phot(MixedObject):
    _title = "new phots"
    _default_tmpl = "public/new/phot"
    def GET(self):
        # TODO: CLEAN WITH FIRE
        self.view.scripts = ["pillbox", "transientbug/phot", "lib/typeahead.min"]
        self.view.stylesheets = ["pillbox"]
        return self.view.render()

    def POST(self):
        url = self.request.getParam("url", None)
        files = self.request.getFile("file")
        title = self.request.getParam("title", "")
        tags = self.request.getParam("tags", "")

        if tags:
            tag = [ bit.lstrip().rstrip() for bit in tags.split(",") ]
        else:
            tag = []

        if url:
            phot = pm.Phot.download_phot(self.request.session.id,
                                         url=url,
                                         title=title,
                                         tags=tag)
        elif files:
            phot = pm.Phot.upload_phot(self.request.session.id,
                                       file_obj=files,
                                       title=title,
                                       tags=tag)

        self.request.session.push_alert("Image is being downloaded...")
        return Redirect("/phots/%s" % phot.filename)
