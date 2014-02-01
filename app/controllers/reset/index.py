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
from seshat_addons.seshat.obj_mods import not_logged_in, template
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect

from errors.general import NotFoundError

import rethinkdb as r
from models.rethink.user import userModel as um
from models.rethink.email import emailModel as em

import utils.short_codes as sc

from seshat_addons.view.template import PartialTemplate


@route()
@not_logged_in("/account")
@template("public/reset/reset", "Password Reset")
class index(MixedObject):
    @HTML
    def GET(self):
        code = self.request.get_param("c")

        if not code:
            self.view.template = "public/reset/request"
            return self.view

        found = r.table(um.User.table).filter({"reset_code": code}).count().run()
        if found:
            return self.view

        else:
            self.request.session.push_alert("That code isn't in the database, want to try requesting a new one?", level="danger")
            return Redirect("/reset")

    @HTML
    def POST(self):
        code = self.request.get_param("c")
        username = self.request.get_param("username")
        password = self.request.get_param("password")

        try:
            user = um.User.from_email(username)

        except NotFoundError:
            self.request.session.push_alert("That email wasn't found in our system. Are you sure its correct?", level="danger")
            return Redirect("/reset")

        if not code:
            user.reset_code = sc.rand_short_code()
            tmpl = PartialTemplate("emails/password_reset")
            tmpl.data = {"user": user}

            content = tmpl.render()

            e = em.Email.new()\
                .send_to(user.id)\
                .send_from("noreply")\
                .set_subject("transientBug.com - Password Reset")\
                .set_text(content)\
                .set_html(content)\
                .queue()

            user.save()

            self.request.session.push_alert("Password reset email sent. Please check your email.")
            self.view.template = "public/reset/sent"
            return self.view

        found = r.table(um.User.table).filter({"reset_code": code}).count().run()
        if found:
            if hasattr(user, "reset_code"):
                if user.reset_code == code:
                    user.set_password(password)

                    self.request.session.push_alert("Password reset, please login with it now to make sure it works :)")
                    return Redirect("/login")

                else:
                    self.request.session.push_alert("That isn't your reset code!", level="danger")
                    return Redirect("/reset")

            else:
                self.request.session.push_alert("That email doesn't have a reset request!", level="danger")
                return Redirect("/reset")

        else:
            self.request.session.push_alert("That code isn't in the database, want to try requesting a new one?", level="danger")
            return Redirect("/reset")


