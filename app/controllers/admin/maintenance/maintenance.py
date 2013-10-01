#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r

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
        current = list(r.table(mm.Maintenance.table).filter({"active": True}).run())

        if current:
            current_msg = mm.Maintenance(**current[0])
        else:
          current_msg = {
              "title": "Maintenance",
              "sub_title": "transientBug is undergoing maintenance and will return shortly..."
          }

        self.view.data.update({"current": current_msg})
        return self.view

    def POST(self):
        ID = self.request.getParam("id", None)
        title = self.request.getParam("title")
        sub_title = self.request.getParam("sub_title")
        contents = self.request.getParam("contents")
        active = self.request.getParam("active", True)

        mm.Maintenance.new_or_update(self.request.session.userID,
                                     ID,
                                     title,
                                     sub_title,
                                     contents,
                                     active)

        self.request.session.pushAlert("Maintenance page updated", level="success")
        return Redirect("/admin/maintenance")
