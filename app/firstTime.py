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
import config.initial as c
import models.rethink.user.userModel as um


def setup():
    print "Setting up fla.gr from config/initial.yaml..."
    initialSetup()
    #bucketSetup()
    print "Done"


def initialSetup():
    print "Setting up inital users"
    for user in c.users:
        newUser = um.User(user["username"], user["password"])
        print "\tAdding new user `%s`"%user["username"]
        print "\t\tpassword `%s`"%user["password"]
        print "\t\tlevel `100` - god"
        newUser.level = 100
        newUser.save()


if __name__ == "__main__":
    setup()
