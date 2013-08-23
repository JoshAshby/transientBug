#!/usr/bin/env python
"""
base collection classes for building collections.
Common functions such as pagination and such live in here.

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""


class baseCollection(object):
    """
    Attempts to be a common ground for collections giving them all a similar
    functionality
    """
    def paginate(self, pageNumber, perPage):
        """
        Paginates self.pail
        """
        pageNumber = int(pageNumber)
        perPage = int(perPage)
        pailVolume = len(self.pail)
        startingPlace = 0
        if pageNumber != 1:
            startingPlace = (pageNumber-1) * perPage
        if startingPlace > pailVolume:
            raise Exception("Starting place outside of collections length.")
        endingPlace = pageNumber*perPage
        if endingPlace > pailVolume:
            endingPlace = pailVolume
        self.pagination = self.pail[startingPlace:endingPlace]
        self.paginateSettings = {"pageNumber": pageNumber, "perPage": perPage}

    def resetPagination(self):
        """
        Resets the pagination, for whatever reason this may be needed,
        It should work just fine.
        """
        self.pagination = []

    @property
    def currentPage(self):
        """
        Simple helper property to return the current page number that the collection
        is paginated on.
        """
        return self.paginateSettings["pageNumber"]

    @property
    def perPage(self):
        """
        Simple helper to return the perpage which the pagination was called with
        """
        return self.paginateSettings["perPage"]

    @property
    def hasNextPage(self):
        """
        Returns true if there are more results past the current paginated results.

        :return: Boolean if there is a next page or not.
        :rtype: Boolean
        """
        perPage = self.paginateSettings["perPage"]
        pageNumber = self.paginateSettings["pageNumber"]
        endingPlace = (pageNumber+1)*perPage
        if endingPlace > len(self.pail):
            return False
        return True

    @property
    def pages(self):
        """
        Returns the number of pages of which the results span

        :return: Integer of how many pages are contained within the
            paginated collection
        :rtype: Int
        """
        pailVolume = float(len(self.pail))
        perPage = float(self.paginateSettings["perPage"])
        if perPage > pailVolume:
            return 1
        return int(round(pailVolume/perPage))

    def preInitAppend(self, drip):
        """
        Pre append hook for adding a redisObject to the internal
        _collection list. Inheriting classes should override this if
        any modification needs to be made on `drip`

        :param drip: a `redisObject` instance
        :type drip: redisObject

        :return: `drip` instance modified or unmodified
        :rtype: redisObject
        """
        return drip

    def postInitAppend(self):
        """
        Post append hook that runs after each `redisObject` is inserted into
        self._collection

        Note: Accepts nothing and returns nothing.
        """
        pass

    def sortBy(self, by, desc=True):
        """
        Sorts the collection by the field specified in `by`

        :param by: The name of the field by which the collection should be
            sorted by
        :type by: Str

        :param desc: If false then the collection is sorted then revered.
        :type desc: Boolean

        :return: The collection after sorting
        :rtype: List
        """
        self._collection.sort(key=lambda x: x[by])
        if not desc:
            self._collection.reverse()
        return self._collection

    def withoutCollection(self, subCol):
        """
        Removes all the elements in subCol from self.pail, resulting in
        in self.pail becoming a list, rather than a RedisList, meaning
        any addObject or delObject made to the collection won't be stored.
        """
        subPail = subCol.pail

        self.pail = list(set(self.pail) - set(subPail))

    @property
    def tub(self):
        return self._collection

    def __iter__(self):
        """
        Emulates an iterator for use in `for` loops and such
        """
        for drip in self._collection:
            yield drip
