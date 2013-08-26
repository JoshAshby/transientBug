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

import models.redis.baseRedisModel as brm
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
        rethinkdb.db_create(con.general.databases["rethink"]["db"]).run()


    dbt = rethinkdb.table_list().run()
    if c.general.reset_users:
        # Reseting users
        if "users" in dbt:
            rethinkdb.table_drop("users").run()

    for table in c.general.tables:
        if not table in dbt:
            rethinkdb.table_create(table).run()


def userSetup():
    print "Setting up inital users..."
    for user in c.general.users:
        try:
            newUser = um.User.new_user(user["username"], user["password"])
            print "Adding new user `%s`"%user["username"]
            print "\tpassword `%s`"%user["password"]
            print "\tlevel `100` - god"
            newUser.level = 100
            newUser.save()
        except userError:
            print "`%s` is already in the system..." % user["username"]


def bucketSetup():
    print "Setting up buckets..."
    buckets = c.general.buckets
    for bucket in buckets:
        print bucket
        print "Adding Bucket:"
        print "\t"  + bucket
        print "\t" + str(buckets[bucket])
        newBucket = brm.redisObject("bucket:" + bucket)

        newBucket["name"] = buckets[bucket]["name"]
        newBucket["value"] = buckets[bucket]["value"]
        newBucket["description"] = buckets[bucket]["description"]

        if buckets[bucket].has_key("users"):
            newBucket["users"] = buckets[bucket]["users"]

    pail = bm.bucketPail("bucket:*:value")
    pail.update()


if __name__ == "__main__":
    setup()
