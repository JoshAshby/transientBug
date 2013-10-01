#!/usr/bin/env python
"""
main index - reroutes to login if you're not logged in

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


@login()
@autoRoute()
class index(HTMLObject):
    """
    Returns base index page.
    """
    _title = "home"
    _defaultTmpl = "public/index/index"
    def GET(self):
        self.view.update({"header": "Coming soon!"})
        return self.view
