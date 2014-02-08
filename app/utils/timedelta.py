#!/usr/bin/env python
"""
Helpful little thing to make creating timedeltas a littl easier?

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from datetime import timedelta
import copy


class Delta(object):
    def __init__(self):
        self._interval = {
            "years": 0,
            "months": 0,
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        }

    def seconds(self, c=None):
        if c is not None:
            self._interval["seconds"] += c
            return self
        else:
            return self._interval["seconds"]

    def minutes(self, c=None):
        if c is not None:
            self._interval["minutes"] += c
            return self
        else:
            return self._interval["minutes"]

    def hours(self, c=None):
        if c is not None:
            self._interval["hours"] += c
            return self
        else:
            return self._interval["hours"]

    def days(self, c=None):
        if c is not None:
            self._interval["days"] += c
            return self
        else:
            return self._interval["days"]

    def weeks(self, c=None):
        if c is not None:
            self._interval["weeks"] += c
            return self
        else:
            return self._interval["weeks"]

    def months(self, c=None):
        if c is not None:
            self._interval["months"] += c
            return self
        else:
            return self._interval["months"]

    def years(self, c=None):
        if c is not None:
            self._interval["years"] += c
            return self
        else:
            return self._interval["years"]

    @property
    def timedelta(self):
        d = copy.copy(self._interval)
      # We'll just assume each month is 4 weeks long...
        m = d.pop("months")
        d["weeks"] += m*4
      # Likewise, we'll assume a year is 365 days
        y = d.pop("years")
        d["days"] += y*365
        return timedelta(**d)

    def __len__(self):
        return self.timedelta.total_seconds()
