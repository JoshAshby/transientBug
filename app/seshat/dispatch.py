#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import routeTable as u

import gevent

import logging
logger = logging.getLogger("seshat.dispatch")

from seshat.requestItem import requestItem
import traceback


import controllers.error as error


def dispatch(env, start_response):
    """
    WSGI dispatcher

    Start off by making the global request object that gets passed around from
    this dispatcher to the controllers to the templater, the request object
    contains all the base logic to pull out the URL request parameters, build
    the session and gather the configuration bucket. It also contains logic for
    building the final header that is returned to the browser when a request is
    finished.

    After this request object has been initialized, we then go through and try
    to find a match in the global urls dictionary which contains key values of
    the regex as the key and the object to route a match on that regex to as
    the value. From there it's either processing and returning the data from
    that controller object or it's returning a 404 or 500 error page.
    """
    request = requestItem(env)
    newHTTPObject = None

    logRequest(request)

    found = u.urls.get(request)
    if found is not None:
        obj = found.__module__+"/"+found.__name__
        newHTTPObject = found(request)
        logObj(request, obj)

    else:
        return error404(request, start_response)

    try:
        content, replyData = newHTTPObject._build()
        if type(content) == tuple:
            request.error = content
            return error500(request, start_response)

        header = replyData[1]
        status = replyData[0]

        if status == "404 NOT FOUND":
            return error404(request, start_response)

        if status == "401 UNAUTHORIZED":
            return error401(request, start_response)

        if content:
            header = request.generateHeader(header, len(content))

        logResponse(request, status, header)

        start_response(status, header)

        gevent.spawn(request.log, status)

        if content: return [str(content)]
        else: return []

    except Exception as e:
        request.error = (e, traceback.format_exc())
        return error500(request, start_response)

    finally:
        del newHTTPObject
        del request


def error404(request, start_response):
    """
    Returns a base 404 not found error page
    """
    newHTTPObject = error.error404(request)
    gevent.spawn(log404, request)

    return reply(newHTTPObject, request, start_response)


def error500(request, start_response):
    """
    Returns the base 500 errorpage with the optional error message in the page.
    These errors are logged in a special error log and there is also a general
    error logged to the default logger.
    """
    newHTTPObject = error.error500(request)
    gevent.spawn(log500, request)

    return reply(newHTTPObject, request, start_response)


def error401(request, start_response):
    """
    Returns the base 401 Unauthorized page.
    """
    newHTTPObject = error.error401(request)
    gevent.spawn(log401, request)

    return reply(newHTTPObject, request, start_response)


def reply(newHTTPObject, request, start_response):
    dataThread = gevent.spawn(newHTTPObject._build)
    dataThread.join()

    content, replyData = dataThread.get()

    header = replyData[1]
    status = replyData[0]

    header = request.generateHeader(header, len(content))

    start_response(status, header)

    del newHTTPObject
    gevent.spawn(request.log, status)
    del request

    return [str(content)]


def logRequest(request):
    logger.debug("""\n\r------- Request ---------------------
    Method: %s
    URL: %s
    PARAMS: %s
    FILES: %s
    IP: %s
    UA: %s
    R: %s
    """ % (request.method, request.url.path, request.params, request.files, request.remote, request.user_agent, request.referer))


def logObj(request, obj):
    logger.debug("""\n\r------- Processing ------------------
    Method: %s
    URL: %s
    Object: %s
    """ % (request.method, request.url.path, obj))


def logResponse(request, status, header):
    header_str = str(header) if status != "200 OK" else ""
    logger.debug("""\n\r--------- Response ---------------------
    URL: %s
    Status: %s %s
    """ % (request.url.path, status, header_str))


def log500(request):
    logger.error("""\n\r-------500 INTERNAL SERVER ERROR--------
    Method: %s
    URL: %s
    IP: %s
    UA: %s
    R: %s
    ERROR: %s
    """ % (request.method, request.url.path, request.remote, request.user_agent, request.referer, request.error))


def log404(request):
    logger.warn("""\n\r-------404 NOT FOUND--------
    Method: %s
    URL: %s
    IP: %s
    UA: %s
    R: %s
    """ % (request.method, request.url.path, request.remote, request.user_agent, request.referer))

def log401(request):
    logger.error("""\n\r-------401 UNAUTHORIZED-------
    Method: %s
    URL: %s
    IP: %s
    UA: %s
    R: %s
    """ % (request.method, request.url.path, request.remote, request.user_agent, request.referer))
