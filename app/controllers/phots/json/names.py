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
from seshat_addons.MixedObject import MixedObject
from seshat_addons.funcMods import JSON

import rethinkdb as r
import models.rethink.phot.photModel as pm


@route()
class names(MixedObject):
    @JSON
    def GET(self):
        raw_names = r.table(pm.Phot.table)\
                     .map(lambda x: x["title"])\
                     .coerce_to('array').run()

        name = self.request.get_param("name")
        if name:
            exists = r.table(pm.Phot.table)\
                      .filter({"title": name})\
                      .map(lambda x: x["title"])\
                      .coerce_to('array').run()

            status = False
            if exists:
                status = True

            return {"status": status}

        else:
            return {"names": raw_names}
