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

from redisORM import RedisModel


@route("/admin/announcements/edit/:id")
@login(["admin"])
@template("admin/announcements/edit", "Site Announcement")
class edit(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "announcements"})
        announcement_id = self.request.id

        announcement = RedisModel(namespace="announcement", key=announcement_id)

        self.view.data = {"announcement": announcement}

        return self.view

    def POST(self):
        ID = self.request.id
        status = self.request.get_param("status", False)
        message = self.request.get_param("message")
        start = self.request.get_param("start")
        end = self.request.get_param("end")

        self.announcements.edit_announcement(ID, message, status, start, end)

        return Redirect("/admin/announcements")
