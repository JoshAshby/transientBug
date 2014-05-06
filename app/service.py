#!/usr/bin/env python2
"""transientBug v2.0.0

Starts up the specified service for transientBug as a long running, non-daemon
process.

Current services:
    main-server      Starts the http server for the main site
    downloader       Starts the phots collection download worker
    emailer          Starts the sites email worker

Usage:
  service.py <service> [-v | --verbose] [-d | --debug]
  service.py --version
  service.py (-h | --help)

Options:
  --help -h          Show this
  --debug -d         Start the service in debug mode
  --verbose -v       Log to the console along with default files

"""
import logging
from docopt import docopt

import config.config as c

from daemons.worker import BaseWorker

from daemons.emailer.emailer import Emailer
from daemons.downloader.downloader import Downloader


class MainServer(BaseWorker):
    name = "main-server"
    def run(self):
        import utils.framework as fw
        fw.init()
        __import__("controllers.controllerMap", globals(), locals())
        fw.server()


daemons = {
    "main-server": MainServer,
    "downloader": Downloader,
    "emailer": Emailer
}


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug v2.0.0')

    c.debug = True if arguments["--debug"] else False

    name = arguments["<service>"] if arguments["<service>"] != "main-server" else None

    level = logging.INFO
    if c.debug:
        level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger()
    logger.setLevel(level)

    if not name:
        fh = logging.FileHandler(c.files.log)
    else:
        name = getattr(c, name)
        fh = logging.FileHandler(name.files.log)

    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if arguments["--verbose"]:
        try:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        except:
            pass

    worker = daemons[arguments["<service>"]]()
    worker.start()
