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

from models.rethink.user import userModel as um

from errors import user as ue


@route()
@login(["admin"])
@template("admin/users/new", "New User")
class new(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "users"})
        return self.view

    @HTML
    def POST(self):
        username = self.request.get_param("username")
        password = self.request.get_param("password")
        email = self.request.get_param("email")
        disable = self.request.get_param("disable", False)

        groups = self.request.get_param("groups")

        if type(groups) is not list:
            groups = [groups]

        groups = [ group.strip(" ").replace(" ", "_").lower() for group in groups if group ]

        try:
            user = um.User.new_user(username, password, email, groups)

        except ue.UsernameError as e:
            self.view.data = {
                "email": email,
                "password": password,
                "disable": disable,
                "error": "username",
                "error_msg": str(e).strip("'")
                }

            return self.view

        except ue.PasswordError as e:
            self.view.data = {
                "email": email,
                "username": username,
                "disable": disable,
                "error": "password",
                "error_msg": str(e).strip("'")
                }

            return self.view

        except ue.EmailError as e:
            self.view.data = {
                "username": username,
                "password": password,
                "disable": disable,
                "error": "email",
                "error_msg": str(e).strip("'")
                }

            return self.view

        self.request.session.push_alert("User created...", level="success")
        return Redirect("/admin/users/"+user.id)
