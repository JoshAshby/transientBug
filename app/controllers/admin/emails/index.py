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

from rethinkORM import RethinkCollection
import models.rethink.email.emailModel as em
from utils.paginate import Paginate


@route()
@login(["email"])
@template("admin/emails/index", "Emails")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "emails"})

        result = RethinkCollection(em.Email)
        page = Paginate(result, self.request, "created", sort_direction="asc")

        self.view.data = {"page": page}

        return self.view

    def POST(self):
        email = em.Email(self.request.id)

        email.queue()

        self.request.session.push_alert("Email queued to be resent.")
        return Redirect("/admin/emails")
