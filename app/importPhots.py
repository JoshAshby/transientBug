import os
import config.config as c

import models.rethink.user.userModel as um
import models.rethink.phot.photModel as pm
import rethinkdb as r

user = r.table(um.User.table).filter({"username": "bug"}).run()
user = list(user)[0]["id"]

f = []
for top, folders, files in os.walk(c.general.dirs["gifs"]):
    f.extend(files)
    break

for fi in f:
    this = pm.Phot.import_phot(user, fi)
    print "Imported %s" % this.filename
