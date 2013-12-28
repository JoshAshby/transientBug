#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c
import logging

logger = logging.getLogger("worker")


class Worker(object):
    name = ""

    def start(self):
        self.run()

    def _setup(self):
        self._queues = (
            ":".join([self.name, "queue"]),
            ":".join([self.name, "command"])
        )

    def run(self):
        self._setup()
        try:
            logger.info("Starting up {} worker...".format(self.name))
            self._poll()

        except KeyboardInterrupt:
            logger.info("Keyboard shutdown")

    def _poll(self):
        while True:
            next_id = c.redis.blpop(self._queues)
            if next_id[0] == self._queues[0]:
                self.data = next_id[1]
                self.build()
            else:
                pass

    def build(self):
        pass

    def _pause(self):
        pass

    def _shutdown(self):
        pass
