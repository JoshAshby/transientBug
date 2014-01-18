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
from seshat.MixedObject import MixedObject
from seshat.objectMods import login, template
from seshat.funcMods import HTML

from seshat.actions import Redirect

from rethinkORM import RethinkCollection
import models.rethink.email.emailModel as em
from utils.paginate import Paginate


@autoRoute()
@login(["email"])
@template("admin/emails/view", "Emails")
class view(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "emails"})

        email = em.Email(self.request.id)

        self.view.data = {"email": email}

        return self.view
