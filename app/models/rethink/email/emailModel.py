"""
http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
from rethinkORM import RethinkModel
import models.utils.promise as promise


class Email(RethinkModel):
    table = "emails"

    @classmethod
    @promise.id_promise("emailer")
    def new_email(cls, service, users, subject="", contents=""):
        """
        Creates a new email and queues it to be sent by the email daemon

        :param service: The local part of the email address this email should be as
        :param users: A list or single `User` instance(s)
        :param subject: The subject for the email
        :param contents: The final contents that make up the body of the email.
        """
        created = arrow.utcnow().timestamp

        if type(users) is list:
            users = [ user.id for user in users ]

        else:
            users = [users.id]

        what = cls.create(users=users,
                          contents=contents,
                          subject=subject,
                          service=service,
                          created=created,
                          sent=None)

        return what

    @property
    def formated_created(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created
