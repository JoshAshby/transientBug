"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkModel
import arrow

import utils.markdownUtils as mdu

import rethinkdb as r


class Note(RethinkModel):
    table = "notes"
    _protectedItems = []

    @classmethod
    def new_note(cls, user="", title="", contents="", public=False, tags=[]):
        """
        """
        created = arrow.utcnow().timestamp
        what = cls.create(user=user,
                          created=created,
                          contents=contents,
                          public=public,
                          tags=tags)

        return what


    def format(self, time_format="human"):
        """
        Formats markdown and dates into the right stuff
        """
        self._formated_text = mdu.markClean(self.about, ['footnotes'])
        if time_format != "human":
            self._formated_created = arrow.get(self.created).format(time_format)
        else:
            self._formated_created = arrow.get(self.created).humanize()
