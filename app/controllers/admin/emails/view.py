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
from seshat_addons.seshat.func_mods import HTML, JSON

import models.rethink.email.emailModel as em


@route()
@login(["email"])
@template("admin/emails/view", "Emails")
class view(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "emails"})

        email = em.Email(self.request.id)

        self.view.data = {"email": email}

        return self.view

    @JSON
    def POST(self):
        email = em.Email(self.request.id)

        email.queue()

        self.request.session.push_alert("Email resent")

        return {"success": True}
