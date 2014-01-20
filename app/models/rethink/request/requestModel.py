"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
import rethinkdb as r
import httpagentparser

from rethinkORM import RethinkModel
import models.rethink.user.userModel as um


class Request(RethinkModel):
    table = "requests"

    @classmethod
    def new_request(cls, user, ip, agent, url, method, referer, status, error):
        created = arrow.utcnow().timestamp

        what = cls.create(user=user,
                          ip=ip,
                          user_agent=agent,
                          url=url,
                          method=method,
                          referer=referer,
                          status=status,
                          error=error,
                          time=created)

        return what

    @property
    def agent(self):
        if not hasattr(self, "_agent"):
            try:
                self._agent = httpagentparser.detect(self.user_agent)
            except:
                self._agent = None

        return self._agent

    @property
    def who(self):
        if self.user:
            if not hasattr(self, "_formated_author"):
                self._formated_author = um.User(self.user)

            return self._formated_author
        else:
            return None

    @property
    def when(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.time).humanize()

        return self._formated_created
