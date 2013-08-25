#!/usr/bin/env python
"""
fla.gr base model with a few classmethods and such to help
    keep a general interface across all couch models


http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c


class baseCouchModel(object):
    """
    Extension of the couchc.database-python Document class to provide a
    bit more of an object interface with the documents, since some
    things such as saving and deleteing the documents doesn't feel
    very object based to me.
    """
    def __init__(self, **kwargs):
        pass

    def collectionsUpdate(self):
        """
        Helper function to make working with objects in collections easier
        """
        pass

    def collectionsDelete(self):
        """
        Helper to aid in working with collections when a model is deleted
        """
        pass

    @classmethod
    def new(cls, **kwargs):
        """
        """
        return cls(**kwargs)

    def save(self):
        """
        Simply a shortcut for saving the document to couch
        """
        self.collectionsUpdate()
        self.store(c.general.couch)

    def delete(self):
        """
        Deletes the current instance
        """
        self.collectionsDelete()
        c.general.couch.delete(self)

    @classmethod
    def getByID(cls, ID):
        """
        If you already know the id of the document you want, then just call
        this and it'll return that document

        :param ID: The document id of the document you want to retrieve
        :return: An instance of `cls` which has the matching document id
        """
        return cls.load(c.general.couch, ID)

    @classmethod
    def findWithView(cls, view, value):
        """
        Searches couchc.database for documents that have the requested username

        :param value: The value to search for in the ORM
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        """
        items = cls.getAll(view, key=value)
        if items:
            if len(items) == 1:
                return items[0]
            else:
                return items
        else:
            items = cls.getAll(view)
            if not items:
                return None
            return cls._search(items, value)

    @classmethod
    def find(cls, value):
        """
        Searches couchc.database for documents that have the requested username

        :param value: The value to search for in the ORM
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        """
        return cls.findWithView(cls._view, value)

    @classmethod
    def getAll(cls, view, key=None):
        """
        Returns either all of the documents under view, or all of the documents
        which match the key
        :param view: The name of the view to use, currently this is the name of the
            couchc.database view, however it can be extended into other areas later on if I
            ever change the underlying database.
        :param key: Optional view key to use
        :return: A list of ORM instances which fall within the given `view`
        """
        if key:
            return list(cls.view(c.general.couch, view, key=key))
        return list(cls.view(c.general.couch, view))

    @classmethod
    def all(cls):
        return cls.getAll(cls._view)
