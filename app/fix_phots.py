#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from rethinkORM import RethinkCollection
from models.rethink.phot.photModel import Phot


if __name__ == "__main__":
    all_phots = RethinkCollection(Phot).fetch()

    for phot in all_phots:
        phot.rename(phot.title)
        phot.tags = [ bit.lstrip().rstrip().replace(" ", "_").lower() for bit in phot.tags ]
        print "Updated phot", phot
        phot.save()
