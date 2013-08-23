#!/usr/bin/env python
"""
TEMPLATE ALL THE THINGS WITH HANDLEBARS!!!!
Uses the mustache templating language to make a base template object by which is
easy to work with in the controllers, and a walker and templateFile objects
which provide automatic reading and rereading in debug mode of template files.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import pystache
import os
import time
import config.config as c
import logging
logger = logging.getLogger(c.general["logName"]+".views")


class templateWalker(object):
    """
    Base walker which goes through the given template path and initializes a
    bucnh of templateFile objects for each mustache template it finds. When a
    template is requested from it later on, such as in the case in the template
    object below, then it returns the template from the templateFile object.
    This is mostly a helper to allow for live file re reading in templateFiles
    """
    def __init__(self, path):
        """
        Walks through `path` looking for mustache templates and adding any that
        it finds into it's `_tmpls` dict in the form of templateFile objects
        """
        self._tmpls = {}
        self._path = path

        base = templateFile(self._path+"base.mustache")
        self._tmpls["base"] = base


        for path, folders, files in os.walk(self._path):
            for directory in folders:
                tempTmpls = {}
                for folder in os.walk(self._path + directory + "/"):
                    allTmpls = folder[2] # files in current directory
                    where = folder[0].split(self._path)[1].rstrip("/") # relative folder path

                    # Everytime we have files in the current directory, go through and see
                    # if any are mustache template files, and if they are then read them into
                    # memory and add them to the watcher
                    for tmpl in allTmpls:
                        parts = tmpl.split(".")
                        extension = parts[len(parts)-1]
                        if extension != "mustache":
                            continue

                        fileBit = folder[0]+"/"+tmpl
                        templateThing = templateFile(fileBit)

                        name = parts[0]
                        tempTmpls[where+"/"+name] = templateThing
            break

            self._tmpls.update(tempTmpls)

    def __getitem__(self, item):
        """
        Mostly a helper to allow for easy access to either a memory stored
        template, or reading in the template freshly each time.
        """
        return self._tmpls[item].template


class templateFile(object):
    def __init__(self, fileBit):
        """
        Reads in fileBit into memory, and sets the modified time for the
        object to that of the file at the current moment.
        """
        self._file = fileBit
        self._mtime = 0

        self.readTemplate()

    @property
    def template(self):
        """
        Returns the template, while reading it in if the file has been
        modified since we first read it in, and only if we are in debug
        mode. Otherwise this will just return the template stored in memory
        from first read/startup.
        """
        if c.general["debug"]:
            self.readTemplate()

        return self._template

    def readTemplate(self):
        """
        Read in the template only if it has been modified since we first
        read it into our `_template`
        """
        mtime = time.ctime(os.path.getmtime(self._file))

        if self._mtime < mtime:
            if c.general["debug"]:
                logger.debug("""\n\r============== Template =================
    Rereading template into memory...
    TEMPLATE:  %s
    OLD MTIME: %s
    NEW MTIME: %s
""" % (self._file, self._mtime, mtime))
            with open(self._file, "r") as openTmpl:
                self._template = unicode(openTmpl.read())
            openTmpl.close()
            self._mtime = mtime


class template(object):
    def __init__(self, template, data):
        self._baseData = {
            "req": data,
            "stylesheets": [],
            "scripts": [],
            "breadcrumbs": ""
        }

        self._render = u""
        self.raw = u""

        self._template = template
        self._base = "base"

    @property
    def skeleton(self):
        return self._base

    @skeleton.setter
    def skeleton(self, value):
        assert type(value) == str
        self._base = value

    @skeleton.deleter
    def skeleton(self):
        self._base = "base"

    @property
    def data(self):
        return self._baseData

    @data.setter
    def data(self, value):
        assert type(value) == dict
        self._baseData.update(value)

    @property
    def scripts(self):
        return self._baseData["scripts"]

    @scripts.setter
    def scripts(self, value):
        assert type(value) == list
        self._baseData["scripts"].extend(value)

    @scripts.deleter
    def scripts(self):
        self._baseData["scripts"] = []

    @property
    def stylesheets(self):
        return self._baseData["stylesheets"]

    @stylesheets.setter
    def stylesheets(self, value):
        assert type(value) == list
        self._baseData["stylesheets"].extend(value)

    @stylesheets.deleter
    def stylesheets(self):
        self._baseData["stylesheets"] = []

    def partial(self, placeholder, template, data):
        data.update(self._baseData)
        self._data[placeholder] = pystache.render(template, data)

    def render(self):
        body = self.raw
        if not self.raw:
            body = tmpls[self._template]

        body = pystache.render(body, self._baseData)

        _data = self._baseData
        _data.update({
            "body"  : body,
        })

        _data["req"].session.renderAlerts()

        self._render = pystache.render(tmpls[self._base], _data)

        return unicode(self._render)

    def __str__(self):
        return unicode(self._render)


def listView(template, collection):
    """
    Takes a collection and renders a list view, of one template per item in
    the collection.
    """
    rendered = u""
    for item in collection:
        rendered += pystache.render(tmpls[template], {"row": item})

    return rendered


def paginateView(collection, template="partials/paginate"):
    """
    Returns a pagination rendered template based off the settings from the
    given collection
    """
    if collection.pages > 2:
        previous = (collection.currentPage-1) if (collection.currentPage > 1) else False

        pages = []
        for page in range(1, (collection.pages+1)):
            pageDict = {"number": page}
            if page == collection.currentPage:
                pageDict.update({"class": "active"})
            pages.append(pageDict)

        last = (collection.currentPage+1) if collection.hasNextPage else False

        data = {"previous": previous,
            "pages": pages,
            "perpage": collection.perPage,
            "next": last,
            "last": collection.pages}

        return unicode(pystache.render(tmpls[template], data))

    else:
        return u""


tmplPath = os.path.dirname(__file__)+"/mustache/"
tmpls = templateWalker(tmplPath)
