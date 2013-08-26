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


@autoRoute()
class view(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "photo"
    _defaultTmpl = "public/screenshots/view"
    def GET(self):
        """
        """
        raw = self.request.id.rsplit(".", 1)
        #if len(raw) > 1:
        name = raw[0].replace("_", " ")
        self.view.data = {"picture": self.request.id, "name": name}
        #else:
            #pass
        return self.view.render()
