"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
import rethinkdb as r

from rethinkORM import RethinkModel
import models.rethink.user.userModel as um
import utils.markdownUtils as mdu

import utils.short_codes as sc


class Note(RethinkModel):
    table = "notes"

    @classmethod
    def new_note(cls, user, title="", contents="", public=False, tags=[]):
        """
        """
        time = arrow.utcnow()
        if not title:
          title = "Untitled Note @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        code_good = False
        code = ""
        while not code_good:
            code = sc.rand_short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          contents=contents,
                          public=public,
                          tags=tags,
                          short_code=code,
                          disable=False)

        return what

    def copy(self):
        time = arrow.utcnow()
        created = time.timestamp

        code_good = False
        code = ""
        while not code_good:
            code = sc.rand_short_code()
            f = r.table(self.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        self.copy = self._data.pop("id")
        self.short_code = code
        self.created = created

    def format_time_spec(self, time_format):
        if not hasattr(self, "_formated_created_spec"):
            self._formated_created_spec = arrow.get(self.created).format(time_format)

        return self._formated_created_spec

    @property
    def formated_author(self):
        if not hasattr(self, "_formated_author"):
            self._formated_author = um.User(self.user).username

        return self._formated_author

    @property
    def formated_tags(self):
        if not hasattr(self, "_formated_tags"):
            self._formated_tags = ', '.join(self.tags)

        return self._formated_tags

    @property
    def formated_time(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created

    @property
    def formated_contents(self):
        if not hasattr(self, "_formated_contents"):
            self._formated_contents = mdu.markClean(self.contents, ['footnotes'])

        return self._formated_contents

    @property
    def formated_short(self):
        if not hasattr(self, "_formated_short_contents"):
            self._formated_short_contents = mdu.markClean(self.contents[:160]+"...", ['footnotes'])

        return self._formated_short_contents
