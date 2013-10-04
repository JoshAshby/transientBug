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

    @classmethod
    def get_current(cls):
        current = list(r.table(cls.table).filter({"active": True}).run())

        if current:
            current_msg = cls(**current[0])
            current_msg.format()
        else:
            current_msg = None

        return current_msg

    @classmethod
    def update(cls, user, title="Maintenance", sub_title="", contents="", active=True):
        if active:
            # Set current active message to inactive
            r.table(cls.table).update(lambda x: {'active': False}).run()

        created = arrow.utcnow().timestamp

        wat = cls.create(user=user,
                         created=created,
                         title=title,
                         sub_title=sub_title,
                         contents=contents,
                         active=active)

        wat.format()

        if active:
            tmpl = PartialTemplate("admin/maintenance/msg")
            tmpl.data = {
                "title": wat.title,
                "sub_title": wat.sub_title,
                "contents": wat._formated_contents,
                "author": wat._formated_author,
                "created": wat._formated_created
            }

            fi = tmpl.render()

            with open(path, 'wb') as msg_file:
                msg_file.write(fi)

        return wat

    @classmethod
    def toggle(cls, id):
        # Set current active message to inactive then toggle this one
        current = cls.get_current()
        if current:
            current.active = False
            current.save()

        wat = Maintenance(id)
        wat.active = True
        wat.save()
        wat.format()

        tmpl = PartialTemplate("admin/maintenance/msg")
        tmpl.data = {
            "title": wat.title,
            "sub_title": wat.sub_title,
            "contents": wat._formated_contents,
            "author": wat._formated_author,
            "created": wat._formated_created
        }

        fi = tmpl.render()

        with open(path, 'wb') as msg_file:
            msg_file.write(fi)

        return wat

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
