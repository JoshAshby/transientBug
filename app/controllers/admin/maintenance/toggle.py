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
from seshat.baseObject import JSONObject
from seshat.objectMods import login

import models.rethink.maintenance.maintenanceModel as mm


@login(["admin"])
@autoRoute()
class toggle(JSONObject):
    def POST(self):
        maintenance_id = self.request.id

        mm.Maintenance.toggle(maintenance_id)
        return {"success": True, "id": maintenance_id}
