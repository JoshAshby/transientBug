"""
Phot model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import arrow
import urlparse

import config.config as c

import rethinkdb as r
from models.rethink.base_interface import BaseInterface
from models.validators.user_validator import UserValidator
from models.validators.tags_validator import TagsValidator
from models.validators.created_validator import CreatedValidator

import utils.short_codes as sc


class Phot(UserValidator, TagsValidator, CreatedValidator, BaseInterface):
    table = "phots"

    _user_field = "user"
    _tags_field = "tags"
    _created_field = "created"

    @classmethod
    def new_phot(cls, user, stuff, title, tags=[]):
        name = title.rstrip().lstrip().replace(" ", "_").lower()

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
        created = time.timestamp

        new_tags = [ tag.lstrip().rstrip().replace(" ", "_").lower() for tag in tags ]

        code_good = False
        code = ""
        while not code_good:
            code = sc.rand_short_code()
            f = r.table(cls.table).filter({"short_code": code}).count().run()
            if f == 0:
                code_good = True

        if not title:
            title = code

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          url=url,
                          tags=new_tags,
                          short_code=code,
                          filename=filename,
                          disable=False)

        if type(stuff) is str:
            c.redis.rpush("downloader:queue", what.id)

        return what

    @property
    def extension(self):
        return self.filename.rsplit(".", 1)[1]

    @property
    def title(self):
        return self._data.get("title")

    @title.setter
    def title(self, title):
        title = title.lower().rstrip().lstrip()
        if self._data.get("title") and title != self._data["title"]:
            new_name = title.replace(" ", "_")

            current_path = ''.join([c.dirs.gifs, self.filename])

            new_filename = ''.join([new_name, ".", self.extension])

            self.filename = new_filename
            self._data["title"] = title

            new_name_path = ''.join([c.dirs.gifs, new_filename])
            os.rename(current_path, new_name_path)

        else:
            self._data["title"] = title

        return title

    @property
    def disable(self):
        if "disable" in self._data:
            return self._data["disable"]

        return False

    @disable.setter
    def disable(self, val):
        self._data["disable"] = val

    def __json__(self):
        d = self._data.copy()
        d.pop("id")
        d.pop("disable") if "disable" in d else None
        d["user"] = self.user.username
        d["source"] = d.pop("url") if "url" in d else ""
        return d
