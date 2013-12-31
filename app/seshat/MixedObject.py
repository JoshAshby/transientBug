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

import base

root_group = "root"


def check_groups(groups, user_groups):
    return len(set(groups).intersection(set(user_groups))) >= 1


class MixedObject(base.BaseHTTPObject):
    _login = (False, False)
    _no_login = False
    _groups = None
    _redirect_url = ""
    _tmpl = None
    _title = None

    def _post_init_hook(self):
        self.head = ("200 OK", [("Content-Type", "text/plain")])


    def _pre_content_hook(self):
        pass

    def _build(self):
        content = ""

        if self._no_login and self.request.session.id:
            self.request.session.push_alert("Thats a page only for non logged in people. Weird huh?")
            if not self._redirect_url:
                self.head = ("303 SEE OTHER", [("Location", "/")])
            else:
                self.head = ("303 SEE OTHER", [("Location", self._redirect_url)])
            return "", self.head

        if self._login[0] and not self.request.session.id:
            if not self._login[1]:
                self.request.session.push_alert("You need to be logged in to view this page.", level="error")

            if not self._redirect_url:
                self.head = ("401 UNAUTHORIZED", [])
            else:
                self.head = ("303 SEE OTHER", [("Location", self._redirect_url)])
            return "", self.head

        if self._groups:
            if not check_groups(self._groups, self.request.session.groups):
                if not self.request.session.has_perm(root_group):
                    self.request.session.push_alert("You are not authorized to perfom this action.", level="error")
                    if not self._redirect_url:
                        self.head = ("401 UNAUTHORIZED", [])
                    else:
                        self.head = ("303 SEE OTHER", [("Location", self._redirect_url)])
                    return "", self.head

        self._pre_content_hook()
        try:
            content = getattr(self, self.request.method)() or ""

            if isinstance(content, actions.BaseAction):
                self.head = content.head

            else:
                content = unicode(content)

        except Exception as e:
            content = (e, traceback.format_exc())

        if self.head[0] not in ["303 SEE OTHER"]:
            del self.request.session.alerts

        return content, self.head
