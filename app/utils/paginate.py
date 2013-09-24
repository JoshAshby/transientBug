#!/usr/bin/env python
"""
helper files for generating pagination from a list of objects

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r
from operator import itemgetter

import urllib
import math

from config.standard import StandardConfig
from views.template import PartialTemplate


class Paginate(StandardConfig):
    def __init__(self, pail, request, sort="", perpage_default=24):
        self._data = {
            "perpage_default": perpage_default,
            "offset": 4,
            "perpage": request.getParam("perpage", perpage_default),
            "page": request.getParam("page", 0, int),
            "sort_direction": request.getParam("dir", "desc"),
            "sort": sort
        }

        self._pail = pail

        self._request = request

        self._calc()

    def _calc(self):
        page_dict = {}

        if type(self._pail) is list:
            if self.sort:
                self._pail.sort(key=itemgetter(self.sort), reverse=True)
            else:
                self._pail.sort()

            if self.sort_direction == "asc":
                self._pail.reverse()
        else:
            di = self.sort
            if self.sort_direction == "desc":
                di = r.asc(self.sort) # Yeah, yeah, I know...
            if self.sort_direction == "asc":
                di = r.desc(self.sort) # Yeah, yeah, I know again... Don't ask

            self._pail = self._pail.order_by(di)

        if self.perpage != "all":
            page_dict["show"] = True

            perpage = int(self.perpage)
            page = int(self.page)

            offset_start = (perpage * page)
            offset_end = offset_start + perpage

            if type(self._pail) is list:
                length = len(self._pail)
            else:
                length = self._pail.count().run()

            if length <= perpage:
                page_dict["show"] = False

            if page != 0:
                page_dict["has_prev"] = True
            else:
                page_dict["has_prev"] = False

            if length > offset_end:
                page_dict["has_next"] = True
            else:
                page_dict["has_next"] = False

            if type(self._pail) is list:
                self._pail = self._pail[offset_start:offset_end]
            else:
                self._pail = self._pail.skip(offset_start).limit(perpage)

            pages = math.ceil(length/perpage)+1

            page_dict["count_start"] = int(max([min([page-math.ceil(self.offset/2)+1, pages-self.offset]), 0]))
            page_dict["count_end"] = int(min([max([page+math.floor(self.offset/2)+1, self.offset]), pages]))

            #if (page-self.offset) <= 0:
                #page_dict["count_start"] = 0
            #else:
                #page_dict["count_start"] = (page-self.offset)

            #if (page+self.offset) <= (length/perpage):
                #page_dict["count_end"] = int(length/perpage)+1
            #else:
                #page_dict["count_end"] = (page+self.offset)

        else:
            page_dict["show"] = False

        if type(self._pail) is not list:
            results = list(self._pail.run())

            self._pail = results

        self._page_dict = page_dict

    @property
    def pail(self):
        return self._pail

    @property
    def query_string(self, extra={}):
        extra_pre = self._request.params.copy()
        extra_pre.pop("page", None)
        extra.update(extra_pre)
        return urllib.urlencode(extra)

    @property
    def options(self):
        tmpl = PartialTemplate("partials/options", self._request)
        tmpl.data.update(self._page_dict)
        tmpl.data.update(self._data)
        tmpl.data.update({"query": self.query_string})

        return tmpl.render()

    @property
    def pager(self):
        tmpl = PartialTemplate("partials/pager", self._request)
        tmpl.data.update(self._page_dict)
        tmpl.data.update(self._data)
        tmpl.data.update({"query": self.query_string})

        return tmpl.render()

    @property
    def paginate(self):
        tmpl = PartialTemplate("partials/paginate", self._request)
        tmpl.data.update(self._page_dict)
        tmpl.data.update(self._data)
        tmpl.data.update({"query": self.query_string})

        return tmpl.render()
