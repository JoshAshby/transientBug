#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

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

import models.rethink.phot.photModel as pm


@login(["phots"])
@autoRoute()
class new(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "new phots"
    _defaultTmpl = "public/gifs/new"
    def GET(self):
        """
        """
        return self.view.render()

    def POST(self):
        url = self.request.getParam("url", None)
        title = self.request.getParam("title", "")
        tags = self.request.getParam("tags", "")

        if tags:
            tag = [ bit.lstrip().rstrip() for bit in tags.split(",") ]
        else:
            tag = []

        phot = pm.Phot.new_phot(self.request.session.userID,
                                url=url,
                                title=title,
                                tags=tag)

        self._redirect("/phots/view/%s" % phot.filename)
        self.request.session.pushAlert("Image is being downloaded...")
        return
