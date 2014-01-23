#!/usr/bin/env python
"""
Just some common various utils for checking rights for a user

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


def check_resource_permission(session, resource):
    """
    Checks to make sure the user is either an admin, root, or owns the resource
    and returns True, otherwise if they don't have the right permissions for
    the resource, then returns False

    
    """
    if session.id == resource.user:
        return True

    if session.has_admin:
        return True

    return False
