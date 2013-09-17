#!/usr/bin/env python
"""
Aid to get flagr setup and running

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as con
import config.initial as c
import models.rethink.user.userModel as um

import models.redis.bucket.bucketModel as bm

import rethinkdb
from models.modelExceptions.userModelExceptions import userError


def setup():
    print "Setting up from config/initial.yaml..."
    initialSetup()
    userSetup()
    bucketSetup()
    print "Done"


def initialSetup():
    print "Setting up database..."
    dbs = rethinkdb.db_list().run()

    if not con.general.databases["rethink"]["db"] in dbs:
        print "Creating database in rethink"
        rethinkdb.db_create(con.general.databases["rethink"]["db"]).run()

    if c.general.flush["users"]:
        print "Reset rethink user table"
        dbt = rethinkdb.table_list().run()
        # Reseting users
        if "users" in dbt:
            rethinkdb.table_drop("users").run()

    print "Creating new rethink tables..."
    dbt = rethinkdb.table_list().run()
    for table in c.general.tables:
        if not table in dbt:
            rethinkdb.table_create(table).run()

    if c.general.flush["redis"]:
        print "Flushing redis..."
        con.general.redis.flushdb()

    if c.general.flush["sessions"]:
        print "Flushing sessions..."
        keys = con.general.redis.keys("session:*")
        for key in keys: con.general.redis.delete(key)

    if c.general.flush["buckets"]:
        print "Flushing buckets..."
        keys = con.general.redis.keys("bucket:*")
        for key in keys: con.general.redis.delete(key)


def userSetup():
    print "Setting up inital users..."
    for user in c.general.users:
        try:
            newUser = um.User.new_user(user["username"], user["password"])
            print "Adding new user `%s`"%user["username"]
            print "\tpassword `%s`"%user["password"]
            print "\tlevel `100` - god"
            print "\tgroups" + str(user["groups"])
            newUser.groups = user["groups"]
            newUser.save()
        except userError:
            print "User `%s` is already in the system..." % user["username"]


def bucketSetup():
    print "Setting up buckets..."
    buckets = c.general.buckets
    pre_buckets = bm.CfgBuckets()
    for ID in buckets:
        bucket = buckets[ID]
        if bucket["name"] in pre_buckets:
            print "\tUpdating Bucket: {}".format(ID)
            pre_buckets.edit(ID,
                             bucket["name"],
                             bucket["description"],
                             bucket["status"])
        else:
            print "\tAdding Bucket: {}".format(ID)
            pre_buckets.new(ID,
                            bucket["name"],
                            bucket["description"],
                            bucket["status"])

if __name__ == "__main__":
    setup()
