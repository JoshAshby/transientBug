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
    _protectedItems = []

    @classmethod
    def download_phot(cls, user, url, title, tags=[]):
        """
        """
        name = title.replace(" ", "_")
        path = ''.join([c.general.dirs["gifs"], name])
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

    def format(self, time_format="human"):
        """
        Formats markdown and dates into the right stuff
        """
        if time_format != "human":
            self._formated_created = arrow.get(self.created).format(time_format)
        else:
            self._formated_created = arrow.get(self.created).humanize()

        self._formated_user = um.User(self.user).username
        self._formated_tags = ', '.join(self.tags)


class ImportPhot(Phot):
    @classmethod
    def import_phot(cls, user, filename):
        """
        """
        parts = filename.rsplit(".", 1)
        if len(parts) >= 1:
            extension = parts[1]
            if extension == "jpeg":
                extension = "jpg"
        else:
            raise Exception("Image extension not found")

        title = parts[0].replace("_", " ")
        created = arrow.utcnow().timestamp

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
                          url="",
                          tags=[],
                          short_code=code,
                          filename=filename)

        return what
