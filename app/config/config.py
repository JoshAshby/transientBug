#!/usr/bin/env python
"""
Seshat config

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import yaml
import redis as red
import rethinkdb as r
import redisORM.redis_model

from utils.standard import StandardODM

def odm_nested_dicts(raw):
    for key, value in raw.iteritems():
        if isinstance(value, dict):
            raw[key] = odm_nested_dicts(value)

    print raw
    return StandardODM(**raw)


def load_yaml_as_object(filename):
    res = None
    with open(filename, "r") as f:
        res = odm_nested_dicts(yaml.load(unicode(f.read())))

    return res

"""
#########################STOP EDITING#####################################
***WARNING***
Don't change these following settings unless you know what you're doing!!!
##########################################################################
"""

current_path = os.path.dirname(__file__) + "/"
base_path = current_path.rsplit("config", 1)[0]

general = None
with open(current_path + "current/config.yaml", "r") as open_config:
    res = yaml.load(unicode(open_config.read()))
    general = StandardODM(**res)

    print odm_nested_dicts(res)


if not general:
    raise Exception("Could not load config.yaml into StandardODM!")


def parse_files(conf):
    if "dirs" in conf:
        for directory in conf.dirs:
            if conf.dirs[directory][0] != "/":
                direct = base_path + conf.dirs[directory]
            else:
                direct = conf.dirs[directory]
            if not os.path.exists(direct):
                os.makedirs(direct)
            conf.dirs[directory] = direct

    if "files" in conf:
        for fi in conf.files:
            extension = conf.files[fi].rsplit(".", 1)
            if "pid" in extension:
                conf.files[fi] = conf.dirs["pid"] + conf.files[fi]
            elif "log" in extension:
                conf.files[fi] = conf.dirs["log"] + conf.files[fi]


rethink = r.connect(db=general["databases"]["rethink"]["db"]).repl()
redis = red.StrictRedis(general["databases"]["redis"]["URL"], db=general["databases"]["redis"]["db"])
redisORM.redis_model.redis = redis

parse_files(general)


downloader = StandardODM(**general.downloader)
emailer = StandardODM(**general.emailer)
dirs = StandardODM(**general.dirs)
files = StandardODM(**general.files)

debug = general["debug"]
send_email = general["send_email"]
