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
from seshat_addons.objectMods import login, template
from seshat_addons.funcMods import HTML
from seshat.actions import Redirect

import models.redis.announcement.announcementModel as am

from utils.paginate import Paginate

import arrow


@route()
@login(["admin"])
@template("admin/announcements/index", "Site Announcements")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "announcements"})
        announcements = am.all_announcements()

        page = Paginate(announcements, self.request, "created")

        self.view.data = {"page": page,
                          "now": arrow.utcnow().format("MM/DD/YYYY HH:mm")}

        return self.view

    def POST(self):
        status = self.request.get_param("status", False)
        message = self.request.get_param("message")
        start = self.request.get_param("start")
        end = self.request.get_param("end")

        if start:
            start = arrow.get(start, 'MM/DD/YYYY HH:mm').to("UTC").timestamp

        if end:
            end = arrow.get(end, 'MM/DD/YYYY HH:mm').to("UTC").timestamp

        self.request.announcements.new_announcement(message, status, start, end)

        return Redirect("/admin/announcements")
