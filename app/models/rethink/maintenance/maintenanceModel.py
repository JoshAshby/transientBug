"""
Maintenace page message model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

import arrow
import rethinkdb as r

from rethinkORM import RethinkModel
import models.rethink.user.userModel as um
import utils.markdownUtils as mdu

from views.template import PartialTemplate


path = ''.join([c.general.dirs["base"], "static/502.html"])


class Maintenance(RethinkModel):
    table = "maintenance"
    _protectedItems = []

    @classmethod
    def new_or_update(cls, user, ID, title="Maintenance", sub_title="", contents="", active=True):
        if active:
            # Set current active message to inactive
            r.table(cls.table).update(lambda x: {'active': False}).run()

        if not ID:
            created = arrow.utcnow().timestamp

            wat = cls.create(user=user,
                             created=created,
                             title=title,
                             sub_title=sub_title,
                             contents=contents,
                             active=active)

        else:
            data = {
              "id": ID,
              "title": title,
              "sub_title": sub_title,
              "contents": contents,
              "active": active
            }
            wat = cls(**data)

        if active:
            tmpl = PartialTemplate("admin/maintenance/msg")
            tmpl.data = {
                "title": title,
                "sub_title": sub_title,
                "content": contents
            }

            fi = tmpl.render()

            with open(path, 'wb') as msg_file:
                msg_file.write(fi)

        wat.save()

        return wat

    def toggle(self):
        # Set current active message to inactive
        r.table(self.table).update(lambda x: {'active': False}).get(self.id).update({"active": True}).run()

    def format(self, time_format="human"):
        """
        Formats markdown and dates into the right stuff
        """
        self._formated_contents = mdu.markClean(self.contents)

        if time_format != "human":
            self._formated_created = arrow.get(self.created).format(time_format)
        else:
            self._formated_created = arrow.get(self.created).humanize()

        self._formated_author = um.User(self.user).username
