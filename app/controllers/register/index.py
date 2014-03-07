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

from errors.user import UsernameError, EmailError

import rethinkdb as r
from models.rethink.user import userModel as um
from models.rethink.email import emailModel as em
from models.rethink.invite import inviteModel as im

from seshat_addons.view.template import PartialTemplate


@route()
@not_logged_in("/account")
@template("public/register/index", "Register")
class index(MixedObject):
    @HTML
    def GET(self):
        code = self.request.get_param("c")

        if self.request.buckets.enablePublicInvites:
            if not code:
                self.view.template = "public/register/closed"
                return self.view

            found = r.table(im.Invite.table).filter({"short_code": code}).coerce_to("array").run()
            if found:
                return self.view

            else:
                self.request.session.push_alert("I couldn't find that invite code. Are you sure you typed it in correctly?", level="danger")
                self.view.template = "public/register/closed"
                return self.view

        else:
            self.view.template = "public/register/closed"

    @HTML
    def POST(self):
        code = self.request.get_param("c")
        username = self.request.get_param("username")
        email = self.request.get_param("email")
        password = self.request.get_param("password")

        if code:
            found = r.table(im.Invite.table).filter({"short_code": code}).coerce_to("array").run()
            if found:
                invite = im.Invite(**found[0])

                if email != invite.email:
                    self.request.session.push_alert("Your email doesn't match the email for that invite!")
                    self.view.template = "public/register/closed"
                    return self.view

                try:
                    user = um.User.new_user(
                            username=username,
                            password=password,
                            email=email,
                            groups=["default"]
                            )

                    user.email = email
                    invite.closed = True

                    tmpl = PartialTemplate("emails/account_registered")
                    tmpl.data = {"user": user}
                    content = tmpl.render()

                    em.Email.new()\
                        .send_to(user.id)\
                        .send_from("noreply")\
                        .set_subject("transientBug.com - Account Registered!")\
                        .set_text(content)\
                        .set_html(content)\
                        .queue()

                    invite.save()
                    user.save()

                    self.request.session.push_alert("Account registered. Please login to make sure everything is okay!")
                    return Redirect("/login")

                except UsernameError:
                    self.view.data = {"error": "username", "error_msg": "That username is already in use, please choose another one."}
                    return self.view

                except EmailError:
                    self.view.data = {"error": "email", "error_msg": "That email is already registered. Maybe try logging in?"}
                    return self.view

        self.view.template = "public/register/closed"
        return self.view
