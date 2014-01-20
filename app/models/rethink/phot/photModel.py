"""
Phot model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow
import urlparse

import config.config as c

import rethinkdb as r
from rethinkORM import RethinkModel
import models.rethink.user.userModel as um

import utils.short_codes as sc


class Phot(RethinkModel):
    table = "phots"

    @classmethod
    def new_phot(cls, user, stuff, title, tags=[]):
        name = title.replace(" ", "_")
        if type(stuff) is str:
            extension = urlparse.urlparse(stuff).path.rsplit(".", 1)[1]
            filename = '.'.join([name, extension])
            url = stuff
        else:
            filename = ''.join([name, ".", stuff.extension])
            path = ''.join([c.dirs.gifs, filename])

            with open(path, 'w+b') as f:
                f.write(stuff.read())
            url = ""

        time = arrow.utcnow()
        if not title:
            title = "Untitled Phot @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        new_tags = [ tag.strip(" ").replace(" ", "_").lower() for tag in tags ]

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
                          url=url,
                          tags=new_tags,
                          short_code=code,
                          filename=filename)

        if type(stuff) is str:
            c.redis.rpush("downloader:queue", what.id)

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
    def author(self):
        if not hasattr(self, "_user"):
            self._user = um.User(self.user)

        return self._user

    def for_json(self):
        d = self._data.copy()
        d.pop("id")
        d.pop("user")
        d["user"] = self.author.username
        d.pop("disable") if "disable" in d else None
        d["source"] = d["url"]
        d["url"] = "https://transientbug.com/i/"+d["filename"]
        return d
