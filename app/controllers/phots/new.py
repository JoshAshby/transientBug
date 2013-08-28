#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login

import requests
from gevent.dns import DNSError


@login(["phots"])
@autoRoute()
class new(HTMLObject):
    """
    Returns base index page listing all gifs
    """
    _title = "new phots"
    _defaultTmpl = "public/gifs/new"
    def GET(self):
        """
        """
        return self.view.render()

    def POST(self):
        url = self.request.getParam("url", None)

        extension = url.rsplit(".", 1)
        if len(extension) >= 1:
            extension = extension[1]
        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "The extension for %s could not be found." % url}
            return self.view

        name = self.request.getParam("name").replace(" ", "_")

        path = ''.join([c.general.dirs["gifs"], name, ".", extension])

        try:
            r = requests.get(url, stream=True)
        except DNSError:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "DNS error"}
            return self.view

        if r.status_code == 200:
            print r.headers
            with open(path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

            loc = ''.join(["/phots/view/", name, ".", extension])

            self.head = ("303 SEE OTHER",
                [("location", loc)])
        else:
            self.view.template = "public/gifs/error"
            self.view.data = {"error": "Something went wrong and the link didn't return a 200 code."}
            return self.view
