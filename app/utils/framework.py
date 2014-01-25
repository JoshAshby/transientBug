#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
#from gevent import monkey; monkey.patch_all()
#from gevent.pywsgi import WSGIServer
#from gevent.pool import Pool

from waitress import serve

import traceback

import logging
import seshat.dispatch as dispatch

import controllers.error as error
import seshat_addons.request_item as r

logger = logging.getLogger("seshat")

import config.config as c


def address_and_port():
    if c.general["port"]:
        port = int(c.general["port"])
    else:
        port = 8000

    if not c.general["address"]:
        address = "127.0.0.1"
    else:
        address = c.general["address"]

    return address, port


def init():
    """
    Server

    Sets up the server and all that messy stuff
    """
    #address, port = address_and_port()

    #if c.general.use_pool:
        #pool = Pool(c.general.max_connections)
    #else:
        #pool = "default"

    dispatch.controller_folder = "controllers"
    dispatch.request_obj = r.RequestItem

    dispatch.route_table.register_error("500", error.error500)
    dispatch.route_table.register_error("404", error.error404)
    dispatch.route_table.register_error("401", error.error401)

    #server = WSGIServer((address, port), dispatch.dispatch, spawn=pool, log=None)

    #return server


def server():
    """
    Server

    Starts the server
    """
    address, port = address_and_port()

    try:
        logger.info("""Now serving py as a WSGI server at %(address)s:%(port)s
        Press Ctrl+c if running as non daemon mode, or send a stop signal
        """ % {"address": address, "port": port})
        #server.serve_forever()
        serve(dispatch.dispatch, host=address, port=port)
        logger.warn("Shutdown py operations.")

    except Exception as exc:
        logger.critical("""Shutdown py operations, here's why: %s""" % exc)

    except:
        logger.critical(traceback.format_exc())

    else:
        logger.critical("""Shutdown py operations for unknown reason!""")
