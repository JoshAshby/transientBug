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
from seshat.baseObject import HTMLObject
from seshat.actions import NotFound

import models.rethink.phot.photModel as pm
import rethinkdb as r


@autoRoute()
class view(HTMLObject):
    _title = "phot"
    _defaultTmpl = "public/gifs/view"
    def GET(self):
        phot = self.request.id

        # check if its a short code by looking for an extension
        # otherwise we assume it's a filename
        if len(phot.rsplit(".")) >= 1:
              f = r.table(pm.Phot.table).filter({"short_code": phot}).run()
              f = list(f)
              if f:
                  self._redirect("/phots/view/%s" % f[0]["filename"])
                  return

        f = list(r.table(pm.Phot.table).filter({"filename": phot}).run())

        if len(f):
            if "disable" in f[0] and f[0]["disable"]:
                self.view.template = "public/gifs/errors/removed"
                return self.view

            photo = pm.Phot(**f[0])

            self.view.data = {"phot": photo}

            if self.request.session.has_phots:
                self.view.scripts = ["phot_del"]
            return self.view

        else:
            return NotFound()
