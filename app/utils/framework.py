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
from waitress import serve

import traceback

import logging
import seshat.dispatch as dispatch
from seshat.error_catcher import catcher as error_catcher
import seshat.route as route

import seshat_addons.view.template as tmpl
from models.redis.session.sessionModel import Session

import controllers.error as error

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
    tmpl.templates_base = c.dirs.templates
    tmpl.dynamic_reloading = True

    route.controller_folder = "controllers"

    dispatch.session_obj = Session

    tmpl.read_in_templates()
    setup_error_pages()


def setup_error_pages():
    error_catcher.register("500", error.error500)
    error_catcher.register("404", error.error404)
    error_catcher.register("401", error.error401)


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
        serve(dispatch.dispatch, host=address, port=port)
        logger.warn("Shutdown py operations.")

    except Exception as exc:
        logger.critical("""Shutdown py operations, here's why: %s""" % exc)

    except:
        logger.critical(traceback.format_exc())
