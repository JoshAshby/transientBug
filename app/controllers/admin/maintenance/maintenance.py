#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkCollection

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login
from seshat.actions import Redirect

import models.rethink.maintenance.maintenanceModel as mm


@login(["admin"])
@autoRoute()
class index(HTMLObject):
    _title = "Maintenance Msg"
    _defaultTmpl = "admin/maintenance/index"
    def GET(self):
        current_msg = mm.Maintenance.get_current()

        if not current_msg:
            current_msg = {
                "title": "Maintenance",
                "sub_title": "transientBug is undergoing maintenance and will return shortly..."
            }

        previous = RethinkCollection(mm.Maintenance, {"active": False})
        previous.order_by("created")
        previous.fetch()

        for item in previous:
            item.format()

        self.view.data.update({"current": current_msg, "previous": previous})
        return self.view

    def POST(self):
        title = self.request.getParam("title")
        sub_title = self.request.getParam("sub_title")
        contents = self.request.getParam("contents")
        active = self.request.getParam("active", True)

        mm.Maintenance.update(self.request.session.userID,
                              title,
                              sub_title,
                              contents,
                              active)

        self.request.session.pushAlert("Maintenance page updated", level="success")
        return Redirect("/admin/maintenance")
