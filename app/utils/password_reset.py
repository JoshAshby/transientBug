"""
User model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import utils.short_codes as sc
from views.template import PartialTemplate

from models.rethink.user import userModel as um
from models.rethink.email import emailModel as em


def send_password_reset(user):
    if type(user) is str:
        user = um.User(user)

    user.reset_code = sc.rand_short_code()
    tmpl = PartialTemplate("emails/password_reset")
    tmpl.data = {"user": user}

    content = tmpl.render()

    address = ["{} <{}>".format(user.username, user.email)]

    em.Email.new_email(service="noreply",
                       addresses=address,
                       subject="transientBug.com - Password Reset",
                       contents=content)

    user.save()
