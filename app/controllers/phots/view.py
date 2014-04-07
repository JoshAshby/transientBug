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
from seshat.actions import NotFound, Redirect, Unauthorized
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from searchers.phots import PhotSearcher
import models.rethink.phot.photModel as pm
import rethinkdb as r


@route()
@template("public/phots/view", "Phot")
class view(MixedObject):
    @HTML
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
                not self.session.has_phots:
            return NotFound()

        photo = pm.Phot(f[0]["id"])

        return {"phot": photo}

    def POST(self):
        if not self.session.has_phots:
            return Unauthorized()

        new_name = self.request.get_param("name")
        tags = self.request.get_param("tags")

        if tags:
            tag = tags.split(",")
        else:
            tag = []


        phot = self.request.id
        if len(phot.rsplit(".")) == 1:
            f = r.table(pm.Phot.table).filter({"short_code": phot})\
                .coerce_to("array").run()
        else:
            f = r.table(pm.Phot.table).filter({"filename": phot})\
                .coerce_to("array").run()

        if f:
            photo = pm.Phot(**f[0])
            photo.rename(new_name)
            photo.tags = tag
            photo.save()

            searcher = PhotSearcher()
            searcher.update(photo)
            searcher.save()

            return Redirect("/phots/"+photo.short_code)

        else:
            return NotFound()
