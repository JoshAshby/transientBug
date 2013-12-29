"""
http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
import config.config as c
from rethinkORM import RethinkModel

from models.rethink.user import userModel as um


class Email(RethinkModel):
    table = "emails"

    @classmethod
    def new_email(cls, service, addresses, subject="", contents=""):
        created = arrow.utcnow().timestamp

        what = cls.create(addresses=addresses,
                          contents=contents,
                          subject=subject,
                          service=service,
                          created=created,
                          sent=None)

        c.redis.rpush("emailer:queue", what.id)

        return what

    @property
    def formated_created(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created
