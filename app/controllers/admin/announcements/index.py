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
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect

import models.redis.announcement.announcementModel as am

from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/announcements/index", "Site Announcements")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "announcements"})
        announcements = am.all_announcements()

        page = Paginate(announcements, self.request, "created")

        self.view.data = {"page": page}

        return self.view

    def POST(self):
        status = self.request.get_param("status", False)
        message = self.request.get_param("message")
        start = self.request.get_param("start")
        end = self.request.get_param("end")

        self.request.announcements.new_announcement(message, status, start, end)

        return Redirect("/admin/announcements")
