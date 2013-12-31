#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import traceback
import actions


class BaseHTTPObject(object):
    """
    Base HTTP page response object
    This determins which REQUEST method to send to,
    along with authentication level needed to access the object.
    """
    def __init__(self, request):
        self.request = request
        self._post_init_hook()

    def _post_init_hook(self):
        pass

    def _build(self):
      content = ""
      self._pre_content_hook()
      try:
          content = getattr(self, self.request.method)()
          if isinstance(content, actions.BaseAction):
              self.head = content.head

          else:
              if not content: content = ""
              if content: content = unicode(content)

      except Exception as e:
          content = (e, traceback.format_exc())

      return content, self.head

    def HEAD(self):
        """
        This is wrong since it should only return the headers... technically...
        """
        return self.GET()

    def GET(self):
        pass

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass
