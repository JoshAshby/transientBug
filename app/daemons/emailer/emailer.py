#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from daemons.worker import Worker

import config.config as c

import models.rethink.email.emailModel as em

from envelopes import Envelope

import logging

logger = logging.getLogger(c.emailer.log_name)


class Emailer(Worker):
    name = "emailer"
    def build(self):
        email = em.Email(self.data)

        logger.info("Sending email {}".format(email.id))

        envelope = Envelope(
            from_addr="{}@transientbug.com".format(email.service),
            to_addr=email.destinations,
            subject=email.subject,
            text_body=email.contents,
        )

        envelope.send('localhost', port=25)

        logger.info("Sent email {}".format(email.id))

