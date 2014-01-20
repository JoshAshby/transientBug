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


from rethinkORM import RethinkCollection
from models.rethink.user import userModel as um

from models.utils import dbUtils as dbu
from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/users/index", "Users")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "users"})
        disabled = self.request.get_param("d", True)
        if disabled:
            q = dbu.rql_where_not(um.User.table, "disable", True)
            res = RethinkCollection(um.User, query=q)

        else:
            res = RethinkCollection(um.User)

        page = Paginate(res, self.request, "username")

        self.view.data = {"page": page}

        return self.view
