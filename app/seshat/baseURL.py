#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
route table container

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import re


class autoURL(object):
    """
    Base container and for generating and storing the url, and regex
    along with the object for the route table.
    """
    def __init__(self, pageObject):
        """
        Attempts to generate the URL from the module name. This uses
        the file hierarchy within the controllers file to represent the URL.
        Controller files must contain the word `Controller` and the folder names
        can not. The actual name of the class within each Controller must be
        the camel case of the files, followed by the actual page name.  

        eg:
            controllers/admin/dev/buckets/bucketsController.py

            contains a class adminDevBucketsIndex which will be routed to
            `/admin/dev/buckets/`
            and also a class adminDevBucketsSave which will be routed to
            `/admin/dev/buckets/save/`
        """
        fullModule = pageObject.__module__
        bits = fullModule.split(".")
        bases = []
        for bit in bits[1:len(bits)-1]:
            bases.append(bit.lower())

        self.url = "/"
        for base in bases:
            self.url += base + "/"

        name = pageObject.__name__

        if name == "index":
            self.url = self.url.rstrip("/")
            self.preRegex = "^" + self.url + "(?:|/)$"
        else:
            self.url += name
            self.preRegex = "^" + self.url +"(?:|/(.*))(?:|/)$"

        self.regex = re.compile(self.preRegex)
        self.pageObject = pageObject
        self.name = name

        try:
            self.title = pageObject._title
        except:
            self.title = "unnamedFalgrPage"

    def __repr__(self):
        return "< baseURL Object, title: " + self.title + " url: " + self.preRegex + " page object: " + self.pageObject.__name__ + " >"
