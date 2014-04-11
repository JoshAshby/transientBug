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

from utils.paginate import Paginate


@route()
@login(["admin"])
@template("admin/buckets/index", "Buckets")
class index(MixedObject):
    @HTML
    def GET(self):
        self.view.partial("sidebar", "partials/admin/sidebar", {"command": "buckets"})
        page = Paginate(self.buckets.list, self.request)
        self.view.data = {"page": page}
        return self.view

    @JSON
    def POST(self):
        bucket_id = self.request.get_param("id")
        self.buckets.toggle(bucket_id)
        return {"success": True, "id": bucket_id}
