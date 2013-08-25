#!/usr/bin/env python
"""
Seshat config

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
"""
First we need to import pythons regex module.
This is used by Seshat to build the routing
table according to what you dictate as the URL
regex below
"""
import os
import yaml
import redis
#import rethinkdb
from couchdb import Server
#from gevent_zeromq import zmq

from standard import StandardConfig

#context = zmq.Context()
#zmqSock = context.socket(zmq.PUB)

current_path = os.getcwd() + "/config/"

general = None
with open(current_path + "config.yaml", "r") as open_config:
    general = StandardConfig(**yaml.load(unicode(open_config.read())))

if not general:
    raise Exception("Could not load config.yaml into StandardConfig!")

#general["rethink"] = rethinkdb.connect(db=general["databases"]["rethink"]["db"]).repl()
try:
    general["couch"] = Server(general["databases"]["couch"]["URL"]+":"+str(general["databases"]["couch"]["port"]))[general["databases"]["couch"]["db"]]
except:
    general["couch"] = Server(general["databases"]["couch"]["URL"]+":"+str(general["databases"]["couch"]["port"]))
general["redis"] = redis.StrictRedis(general["databases"]["redis"]["URL"], db=general["databases"]["redis"]["db"])
#general["zeromq"] = zmqSock.bind(general["sockets"]["URL"]+":"+str(general["sockets"]["port"]))

for directory in general.dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)

"""
#########################STOP EDITING#####################################
***WARNING***
Don't change these following settings unless you know what you're doing!!!
##########################################################################
"""
urls = []
