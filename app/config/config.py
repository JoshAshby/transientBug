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

from utils.standard import StandardODM


"""
#########################STOP EDITING#####################################
***WARNING***
Don't change these following settings unless you know what you're doing!!!
##########################################################################
"""

current_path = os.path.dirname(__file__) + "/"
base_path = current_path.rsplit("config", 1)[0]

general = None
with open(current_path + "config.yaml", "r") as open_config:
    general = StandardODM(**yaml.load(unicode(open_config.read())))

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

parse_files(general)


# I need a better way to get around this. Maybe time to write something that
# looks for dicts within the yaml, and converts them to a ODM and then attaches
# that ODM to the parent as an attribute
downloader = StandardODM(**general.downloader)
parse_files(downloader)
downloader.files = StandardODM(**downloader.files)
downloader.dirs = StandardODM(**downloader.dirs)

emailer = StandardODM(**general.emailer)
parse_files(emailer)
emailer.files = StandardODM(**emailer.files)
emailer.dirs = StandardODM(**emailer.dirs)

indexer = StandardODM(**general.indexer)

dirs = StandardODM(**general.dirs)
files = StandardODM(**general.files)

debug = general["debug"]
send_email = general["send_email"]
