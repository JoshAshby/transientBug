#!/usr/bin/env python2
"""
Controller for authentication login

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template, not_logged_in
from seshat_addons.seshat.func_mods import HTML
from seshat.actions import Redirect
import errors.session as se


@route()
@not_logged_in("/")
@template("public/auth/login", "Login")
class login(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("about", "public/about/about")
        return self.view

    @HTML
    def POST(self):
        passwd = self.request.get_param("password")
        name = self.request.get_param("username")

        if not passwd and not name:
            self.view.partial("about", "public/about/about")
            return self.view

        exc = ""
        try:
            self.session.login(name, passwd)
            self.session.push_alert("Welcome back, %s!" % name,
                                           "Ohia!", "success")

            where = self.request.get_param("return-to", "/")

            return Redirect(where)

        except se.UsernameError as e:
            exc = e
            self.view.data = {"username" : name}
            self.view.data = {"usernameError": True}

        except se.PasswordError as e:
            exc = e
            self.view.data = {"username": name}
            self.view.data = {"passwordError": True}

        except se.DisableError as e:
            exc = e
            self.view.data = {"banError": True}

        exc = unicode(exc).strip("'")

        self.session.push_alert("%s <br/>Please try again." % exc,
                                       "Uh oh...", "error")
        return self.view
