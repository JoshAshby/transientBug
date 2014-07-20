#!/usr/bin/env python
"""transientBug Bag Manager

Util for setting up, and updating the databases

Usage:
    bags_manager.py (rethink|redis) [-v | --verbose] [-d | --debug]
    bags_manager.py --version
    bags_manager.py (-h | --help)

Options:
    --help -h          Show this
    --debug -d         Start the service in debug mode
    --verbose -v       Log to the console along with default files

"""
import logging
from docopt import docopt
import rethinkdb

import yaml
from utils.standard import StandardODM

import config.config as c

import models.rethink.user.userModel as um
import models.redis.bucket.bucketModel as bm

from errors.user import UsernameError


logger = logging.getLogger(c.general.logName+".bags_manager")


rethink_bags = c.load_yaml_as_object("config/current/bags/rethink.yaml")
redis_bags = c.load_yaml_as_object("config/current/bags/redis.yaml")


if not rethink_bags or not redis_bags:
    raise Exception("Can't load bag files!")


def create_rethink_database():
    current_databases = rethinkdb.db_list().run()
    logger.debug("Current databases in rethink: {}".format(current_databases))
    database_name = c.general.databases["rethink"]["db"]

    if not database_name in current_databases:
        logger.info("\tDatabase {} does not exist, creating...".format(database_name))
        rethinkdb.db_create(database_name).run()
        logger.debug("\tDatabase {} created".format(database_name))


def create_rethink_tables():
    current_tables = rethinkdb.table_list().coerce_to("array").run()
    logger.debug("Current tables in rethink: {}".format(current_tables))

    tables_to_create = list(set(rethink_bags.tables.keys()).difference(set(current_tables)))
    logger.info("Creating these new tables in rethink: {}".format(tables_to_create))

    for table in tables_to_create:
        rethinkdb.table_create(table).run()
        logger.debug("Table {} created in rethink".format(table))


def flush_rethink_tables():
    tables_to_flush = [ table for table, flush in rethink_bags.flush.iteritems() if flush ]
    logger.debug("Tables that should be flushed: {}".format(tables_to_flush))

    current_tables = rethinkdb.table_list().coerce_to("array").run()
    logger.debug("Current tables in rethink: {}".format(current_tables))

    flushing_tables = list(set(current_tables).intersection(tables_to_flush))
    logger.info("Flushing tables in rethink: {}".format(flushing_tables))

    for table in flushing_tables:
        rethinkdb.table_drop(table).run()
        rethinkdb.table_create(table).run()
        logger.debug("Table {} flushed in rethink".format(table))


def user_setup():
    logger.info
    for user in rethink_bags.tables["users"]:
        try:
            um.User.new_user(user["username"], user["password"], user["email"], user["groups"])
            logger.debug("\n".join([
                "Adding new user `%s`"%user["username"],
                "\tpassword `%s`"%user["password"],
                "\temail `%s`"%user["email"],
                "\tgroups" + str(user["groups"])]))
        except UsernameError:
            logger.debug("User `{}` is already in the system...".format(user["username"]))


def flush_redis_keyspaces():
    keyspaces_to_flush = [ keyspace for keyspace, flush in redis_bags.flush.iteritems() if flush ]
    logger.debug("Flushing these redis keyspaces: {}".format(keyspaces_to_flush))

    for keyspace in keyspaces_to_flush:
        keyspace += ":*"
        c.redis.delete(keyspace)
        logger.debug("Flushed keyspace {} in redis".format(keyspace))


def redis_buckets_setup():
    logger.info("Setting up buckets in redis...")

    buckets = redis_bags.buckets

    pre_buckets = bm.CfgBuckets()
    for ID in buckets:
        bucket = buckets[ID]
        if ID in pre_buckets:
            logger.debug("\tUpdating Bucket: {} with bag:\n\t{}".format(ID, bucket))
            pre_buckets.edit(ID,
                             bucket["name"],
                             bucket["description"],
                             bucket["status"])

        else:
            logger.debug("\tAdding Bucket: {} with bag:\n\t{}".format(ID, bucket))
            pre_buckets.new(ID,
                            bucket["name"],
                            bucket["description"],
                            bucket["status"])


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug bags manager v0.0.0')

    c.debug = True if arguments["--debug"] else False

    level = logging.INFO
    if c.debug:
        level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger.setLevel(level)

    fh = logging.FileHandler(c.files.log)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if arguments["--verbose"]:
        try:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        except:
            pass

    if arguments["rethink"]:
        create_rethink_database()
        flush_rethink_tables()
        create_rethink_tables()
        user_setup()

    if arguments["redis"]:
        flush_redis_keyspaces()
        redis_buckets_setup()
