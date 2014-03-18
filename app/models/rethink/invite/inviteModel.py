"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
from models.validators.user_validator import UserValidator
from models.validators.created_validator import CreatedValidator
from models.rethink.email import emailModel as em

from seshat_addons.view.template import PartialTemplate

import utils.short_codes as sc


class Invite(UserValidator, CreatedValidator, BaseInterface):
    table = "invites"

    _user_field = "user_id"
    _created_field = "created"

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
    def email(self):
        return em.Email(self.email_id)
