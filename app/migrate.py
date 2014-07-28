#!/usr/bin/env python
"""Migrate

Util to list and run migrations in the migrations directory.

Usage:
    migrate.py (list) [-v | --verbose] [-d | --debug]
    migrate.py --version
    migrate.py (-h | --help)

Options:
    --help -h          Show this
    --debug -d         Start the service in debug mode
    --verbose -v       Log to the console along with default files
"""
import logging
import os
from docopt import docopt

import config.config as c

from utils.mass_updater import MassUpdater

logger = logging.getLogger(c.general.logName+".migrate")

migrations_dir = 'migrations/'


def list_migrations():
    print "Current migrations:"

    files = os.listdir(migrations_dir)
    files.pop(files.index("__init__.py"))

    for f in files:
        print "\t"+f


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug v2.0.0')

    c.debug = True if arguments["--debug"] else False

    level = logging.INFO
    if c.debug:
        level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger()
    logger.setLevel(level)

    fh = logging.FileHandler(c.files.log)
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

    if arguments['list']:
        list_migrations()
