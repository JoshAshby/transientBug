#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
modifying decorators for HTTP method functions

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import json
from views.template import template
import actions


def HTML(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        data = {"title": self._title if self._title else "Untitled"}
        self.view = template(self._tmpl, self.request, data)

        res = f(*args, **kwargs)

        self.head = (self.head[0], [("Content-Type", "text/html")])

        if isinstance(res, template):
            string = res.render()
            del res
            return string
        else:
            return res

    return wrapper


def JSON(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        res = f(*args, **kwargs)
        if isinstance(res, actions.Unauthorized) or isinstance(res, actions.NotFound):
            return [{"error": res.head[0]}]

        if type(res) is dict or type(res) is list:
            self.head = (self.head[0], [("Content-Type", "application/json")])
            return json.dumps([res])

        else:
            return res

    return wrapper
