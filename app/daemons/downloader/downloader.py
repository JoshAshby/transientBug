#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from daemons.worker import RedisWorker

import config.config as c

import models.rethink.phot.photModel as pm

import requests
#import cStringIO

import logging

logger = logging.getLogger(c.downloader.log_name)


class Downloader(RedisWorker):
    name = "downloader"
    def build(self):
        phot = pm.Phot(self.data)

        path = ''.join([c.dirs.gifs, phot.filename])

        logger.info("Downloading photo {}".format(phot.url))
        req = requests.get(phot.url)

        if req.status_code == 200:
            with open(path, 'w+b') as f:
                f.write(req.content)

            logger.info("Download for photo {} finished.".format(phot.url))

        else:
            logger.warn("Resource {} failed with status code: {}".format(phot.url, req.status_code))
