"""
Phot model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkModel
import models.rethink.user.userModel as um
import arrow

import rethinkdb as r

import requests

import config.config as c

import models.utils.dbUtils as dbu

import gevent


def download_photo(url, filename):
    path = ''.join([c.general.dirs["gifs"], filename])

    req = requests.get(url, stream=True)

    if req.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in req.iter_content():
                f.write(chunk)
    else:
        raise Exception("Image could not be found")


class Phot(RethinkModel):
    table = "phots"
    _protectedItems = []

    @classmethod
    def new_phot(cls, user, url, title="", tags=[]):
        """
        """
        extension = url.rsplit(".", 1)
        if len(extension) >= 1:
            extension = extension[1]
            if extension == "jpeg":
                extension = "jpg"
        else:
            raise Exception("Image extension not found")

        name = title.replace(" ", "_")
        filename = ''.join([name, ".", extension])

        if url and url is not None:
            gevent.spawn(download_photo, url, filename)
        else:
            raise Exception("URL required")

        time = arrow.utcnow()
        if not title:
          title = "Untitled Phot @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        code_good = False
        code = ""
        while not code_good:
            code = dbu.short_code()
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
                          extension=extension,
                          filename=filename)

        return what

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
            code = dbu.short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          url="",
                          tags=[],
                          short_code=code,
                          extension=extension,
                          filename=filename)

        return what

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
