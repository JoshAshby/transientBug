"""
Phot model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import gevent
import arrow
import urlparse

import config.config as c

import rethinkdb as r
from rethinkORM import RethinkModel
import models.rethink.user.userModel as um

import utils.short_codes as sc
import utils.files as fu


class Phot(RethinkModel):
    table = "phots"

    @classmethod
    def download_phot(cls, user, url, title, tags=[]):
        name = title.replace(" ", "_")
        path = ''.join([c.general.dirs["gifs"], name])

# TODO: Move the download stuff to a daemon.
        gevent.spawn(fu.download_file, url, path)

        extension = urlparse.urlparse(url).path.rsplit(".", 1)[1]
        filename = '.'.join([name, extension])

        time = arrow.utcnow()
        if not title:
            title = "Untitled Phot @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        code_good = False
        code = ""
        while not code_good:
            code = sc.rand_short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        new_tags = []
        for tag in tags:
            new_tags.append(tag.replace(" ", "_"))

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          url=url,
                          tags=new_tags,
                          short_code=code,
                          filename=filename)

        return what

    @classmethod
    def upload_phot(cls, user, file_obj, title, tags=[], url=""):
        name = title.replace(" ", "_")
        filename = ''.join([name, ".", file_obj.extension])

        path = ''.join([c.general.dirs["gifs"], filename])
        gevent.spawn(fu.write_file, file_obj, path)

        time = arrow.utcnow()
        if not title:
            title = "Untitled Phot @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        code_good = False
        code = ""
        while not code_good:
            code = sc.rand_short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        new_tags = []
        for tag in tags:
            new_tags.append(tag.replace(" ", "_"))

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          url=url,
                          tags=new_tags,
                          short_code=code,
                          filename=filename)

        return what

    @property
    def extension(self):
        return self.filename.rsplit(".", 1)[1]

    @property
    def formated_created(self):
        if not hasattr(self, "_formated_created"):
            self._formated_created = arrow.get(self.created).humanize()

        return self._formated_created

    @property
    def user(self):
        if not hasattr(self, "_user"):
            self._user = um.User(self.user).username

        return self._user
