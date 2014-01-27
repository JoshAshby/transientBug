"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from rethinkORM import RethinkModel
import models.rethink.user.userModel as um
import utils.markdown_utils as md

import utils.short_codes as sc


class Note(RethinkModel):
    table = "notes"

    @classmethod
    def new_note(cls, user, title="", contents="", draft=True, public=False, toc=False, has_comments=False, tags=None):
        if not tags:
            tags = []

        time = arrow.utcnow()
        if not title:
            title = "Untitled Note @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        new_tags = [ tag.replace(" ", "_").lower() for tag in tags ]

        code = sc.generate_short_code(cls.table)

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          contents=contents,
                          public=public,
                          tags=new_tags,
                          table_of_contents=toc,
                          draft=draft,
                          has_comments=has_comments,
                          short_code=code,
                          disable=False,
                          reported=False)

        return what

    def copy(self, user):
        copy_data = self._data.copy().pop("id").pop("user")
        copy_data["short_code"] = sc.generate_short_code(self.table)
        copy_data["created"] = arrow.utcnow().timestamp
        copy_data["user"] = user.id

        copy = Note(**copy_data)

        return copy

    @property
    def author(self):
        if not hasattr(self, "_formated_author"):
            self._formated_author = um.User(self.user)

        return self._formated_author

    @property
    def formated_time(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created

    @property
    def formated_contents(self):
        if not hasattr(self, "_formated_contents"):
            self._formated_contents = md.markdown(self.contents)

        return self._formated_contents
