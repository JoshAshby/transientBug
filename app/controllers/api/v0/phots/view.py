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
from seshat.actions import NotFound
from seshat_addons.seshat.func_mods import JSON

import models.rethink.phot.photModel as pm
import rethinkdb as r


@route()
class view(MixedObject):
    @JSON
    def GET(self):
        phot = self.request.id

        # check if its a short code by looking for an extension
        # otherwise we assume it's a filename
        if len(phot.rsplit(".")) == 1:
            f = r.table(pm.Phot.table).filter({"short_code": phot})\
                .coerce_to("array").run()
        else:
            f = r.table(pm.Phot.table).filter({"filename": phot})\
                .coerce_to("array").run()

        if not f:
            return NotFound()

        if "disable" in f[0] and f[0]["disable"] and \
                not self.session.has_group("phots"):
            return NotFound()

        photo = pm.Phot(**f[0])

        return photo
