"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
from rethinkORM import RethinkModel
import models.utils.promise as promise
import models.rethink.user.userModel as um


class Email(RethinkModel):
    table = "emails"

    @classmethod
    def new(cls):
        em = cls()
        em.content = {"html": "", "text": ""}
        em.bcc_addresses = []
        em.cc_addresses = []
        em.to_addresses = []
        em.service = None
        em.subject = None
        em.created = None
        return em

    def send_to(self, addresses):
        if type(addresses) is not list:
            self.to_addresses = [ addresses ]
        else:
            self.to_addresses = addresses

        return self

    def send_bcc(self, addresses):
        if type(addresses) is not list:
            self.bcc_addresses = [ addresses ]
        else:
            self.bcc_addresses = addresses

        return self

    def send_cc(self, addresses):
        if type(addresses) is not list:
            self.cc_addresses = [ addresses ]
        else:
            self.cc_addresses = addresses

        return self

    def send_from(self, who):
        self.service = who
        return self

    def set_text(self, c):
        self.content["text"] = c
        return self

    def set_html(self, c):
        self.content["html"] = c
        return self

    def set_subject(self, s):
        self.subject = s
        return self

    @promise.id_promise("emailer")
    def queue(self):
        self.created = arrow.utcnow().timestamp
        self.save()
        return self

    @property
    def formated_created(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created

    @property
    def who(self):
        fin = []
        for user in self.to_addresses:
            fin.append(um.User(user).email)

        return fin

    @property
    def who_cc(self):
        fin = []
        for user in self.cc_addresses:
            fin.append(um.User(user).email)

        return fin

    @property
    def who_bcc(self):
        fin = []
        for user in self.bcc_addresses:
            fin.append(um.User(user).email)

        return fin
