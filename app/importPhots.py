#!/usr/bin/env python
"""
Aid to get all photos in the gif directory imported into rethinkdb

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c

import models.rethink.user.userModel as um
import models.rethink.phot.photModel as pm
import rethinkdb as r

user = r.table(um.User.table).filter({"username": "bug"}).run()
user = list(user)[0]["id"]

print "Reset rethink phots table"
dbt = r.table_list().run()
if pm.Phot.table in dbt:
    r.table_drop(pm.Phot.table).run()

f = []
for top, folders, files in os.walk(c.general.dirs["gifs"]):
    f.extend(files)
    break

for fi in f:
    print "Working on %s" % fi
    this = pm.Phot.import_phot(user, fi)
    print "\t Imported %s" % this.filename
