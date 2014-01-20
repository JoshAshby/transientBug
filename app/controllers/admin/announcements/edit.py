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
from seshat_addons.mixed_object import MixedObject
from seshat_addons.obj_mods import login, template
from seshat_addons.func_mods import HTML
from seshat.actions import Redirect

import models.redis.baseRedisModel as brm

import arrow


@route()
@login(["admin"])
@template("admin/announcements/edit", "Site Announcement")
class edit(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "announcements"})
        announcement_id = self.request.id

        announcement = brm.SeshatRedisModel("announcement:"+announcement_id)

        if announcement.start:
            announcement._formated_start = arrow.get(announcement.start)\
                .format("MM/DD/YYYY HH:mm")
        if announcement.end:
            announcement._formated_end = arrow.get(announcement.end)\
                .format("MM/DD/YYYY HH:mm")

        self.view.data = {"announcement": announcement,
                          "now": arrow.utcnow().format("MM/DD/YYYY HH:mm")}

        return self.view

    def POST(self):
        ID = self.request.id
        status = self.request.get_param("status", False)
        message = self.request.get_param("message")
        start = self.request.get_param("start")
        end = self.request.get_param("end")

        if start:
            start = arrow.get(start, 'MM/DD/YYYY HH:mm').to("UTC").timestamp

        if end:
            end = arrow.get(end, 'MM/DD/YYYY HH:mm').to("UTC").timestamp

        self.request.announcements.edit_announcement(ID, message, status, start, end)

        return Redirect("/admin/announcements")
