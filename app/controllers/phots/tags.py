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
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
@template("public/phots/tags", "Phots Tags")
class tags(MixedObject):
    @HTML
    def GET(self):
        orig = self.request.get_param("filter", "all")
        filt = dbu.phot_filter(orig)

        q = dbu.rql_where_not(pm.Phot.table, "disable", True)
        q = q.filter(lambda doc: doc["filename"].match(filt))

        all_tags = q\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        self.view.template = "public/phots/tags"

        self.view.data = {"tags": all_tags}

        return self.view
