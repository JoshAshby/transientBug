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
from seshat.actions import Redirect
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import login, template
from seshat_addons.seshat.func_mods import HTML

from rethinkORM import RethinkCollection
from models.rethink.invite import inviteModel as im

from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/invites/index", "Invites")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "invites"})

        res = RethinkCollection(im.Invite)
        page = Paginate(res, self.request, "created")

        self.view.data = {"page": page}

        return self.view

    def POST(self):
        try:
            email = self.request.get_param("email")

            if email:
                im.Invite.new(email)

            self.request.session.push_alert("Invite sent!")
            return Redirect("/admin/invites")
        except Exception as e:
            print e
