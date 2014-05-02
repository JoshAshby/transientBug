#!/usr/bin/env python
"""
Aid to get transientBug setup and running, along with keeping the database updated

TODO: FIXTHISSHITPLS (for the love of all small furry things, this should probably be rewritten before it causes some mass chaos which in turn causes some small deity to get pissed off and smite a bunny).

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as con
import config.initial as c
import models.rethink.user.userModel as um

import models.redis.bucket.bucketModel as bm

import rethinkdb
from errors.user import UsernameError


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

    dbt = list(rethinkdb.table_list().run())
    for db in c.general.flush["rethink"]:
        if c.general.flush["rethink"][db]:
            print "Flushing rethink "+db+" table..."
            if db in dbt:
                rethinkdb.table_drop(db).run()
                dbt.pop(dbt.index(db))

    print "Creating new rethink tables..."
    for table in c.general.tables:
        if not table in dbt:
            print "Creating table {}".format(table)
            rethinkdb.table_create(table).run()

    for key in c.general.flush["redis"]:
        if c.general.flush["redis"][key]:
            print "Flushing redis "+key+" keys..."
            keys = con.redis.keys(key+":*")
            for key in keys: con.redis.delete(key)


def userSetup():
    print "Setting up inital users..."
    for user in c.general.users:
        try:
            um.User.new_user(user["username"], user["password"], user["email"], user["groups"])
            print "Adding new user `%s`"%user["username"]
            print "\tpassword `%s`"%user["password"]
            print "\temail `%s`"%user["email"]
            print "\tgroups" + str(user["groups"])
        except UsernameError:
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
