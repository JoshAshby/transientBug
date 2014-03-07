"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
from models.rethink.user import userModel as um
from models.rethink.email import emailModel as em

from seshat_addons.view.template import PartialTemplate

import utils.short_codes as sc


class Invite(BaseInterface):
    table = "invites"

    @classmethod
    def new(cls, email):
        short = sc.generate_short_code(cls.table)

        # TODO: verify email is at least a valid email

        what = super(Invite, cls).new(short_code=short,
                          email_address=email,
                          created=arrow.utcnow().timestamp,
                          closed=False,
                          user_id=None,
                          email_id=None)

        tmpl = PartialTemplate("emails/invite")
        tmpl.data = {"invite": what}
        content = tmpl.render()

        e = em.Email.new()\
            .send_to(email)\
            .send_from("noreply")\
            .set_subject("transientBug.com - Invite to Register!")\
            .set_text(content)\
            .set_html(content)\
            .queue()

        what.email_id = e.id

        what.save()

        return what

    @property
    def created(self):
        if not hasattr(self, "_formated_created") or self._formated_created is None:
            self._formated_created = arrow.get(self._data["created"])

        return self._formated_created

    @created.setter
    def created(self, val):
        """
        val should be a unix timestamp of the created datetime instance
        """
        self._formated_created = val
        self._data["created"] = val

    @property
    def user(self):
        if self.user_id:
            if not hasattr(self, "_user") or self._user is None:
                try:
                    self._user = um.User(self.user_id)

                except:
                    self._user = None

            return self._user

        else:
            return None

    @property
    def email(self):
        return em.Email(self.email_id)
