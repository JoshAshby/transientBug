"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkModel
import models.rethink.user.userModel as um
import arrow

import utils.markdownUtils as mdu

import rethinkdb as r

import models.utils.dbUtils as dbu


class Note(RethinkModel):
    table = "notes"
    _protectedItems = []

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
            code = dbu.short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          contents=contents,
                          public=public,
                          tags=tags,
                          short_code=code)

        return what

    def format(self, time_format="human", length=160):
        """
        Formats markdown and dates into the right stuff
        """
        self._formated_contents = mdu.markClean(self.contents, ['footnotes'])

        self._formated_short_contents = mdu.markClean(self.contents[:length]+"...", ['footnotes'])
        if time_format != "human":
            self._formated_created = arrow.get(self.created).format(time_format)
        else:
            self._formated_created = arrow.get(self.created).humanize()

        self._formated_author = um.User(self.user).username
        self._formated_tags = ', '.join(self.tags)
