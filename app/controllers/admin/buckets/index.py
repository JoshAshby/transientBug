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
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

from utils.paginate import pager


@login(["admin"])
@autoRoute()
class index(HTMLObject):
    _title = "Buckets"
    _defaultTmpl = "admin/buckets/index"
    def GET(self):
        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)

        f, page_dict = pager(self.request.buckets.list, perpage, page)

        self.view.data = {"buckets": f, "page": page_dict}
        self.view.scripts = ["admin/bucket"]

        return self.view
