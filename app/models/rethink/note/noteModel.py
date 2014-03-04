"""
Notes model for use in seshat built off of rethinkdb

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
import models.rethink.user.userModel as um
import utils.markdown_utils as md

import utils.short_codes as sc


class Note(BaseInterface):
    table = "notes"

    @classmethod
    def new_note(cls, user, title="", contents="", draft=True, public=False,
            toc=False, has_comments=False, tags=None, theme="default"):
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
                          theme=theme,
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
        return self.user

    @author.setter
    def author(self, val):
        self.user = val

    @property
    def tags(self):
        return self._data.get("tags")

    @tags.setter
    def tags(self, val):
        tag = [ bit.lstrip().rstrip().lower().replace(" ", "_") for bit in val ]
        self._data["tags"] = tag

    @property
    def user(self):
        if not hasattr(self, "_user") or self._user is None:
            self._user = um.User(self._data.get("user"))
        return self._user

    @user.setter
    def user(self, val):
        if isinstance(val, um.User):
            self._data["user"] = val.id
        else:
            self._data["user"] = val

        self._user = um.User(self._data["user"])

    @property
    def created(self):
        if not hasattr(self, "_formated_created") or self._formated_created is None:
            self._formated_created = arrow.get(self._data["created"])

        return self._formated_created

    @created.setter
    def created(self, val):
        """
        val should be a unix timestamp of the created datetime instance
        """
        self._formated_created = val
        self._data["created"] = val

    @property
    def contents(self):
        if not hasattr(self, "_formated_contents"):
            self._formated_contents = md.markdown(self._data["contents"])

        return self._formated_contents

    @contents.setter
    def contents(self, val):
        self._data["contents"] = val

    @property
    def raw(self):
        return self._data["contents"]
