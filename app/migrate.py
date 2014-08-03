#!/usr/bin/env python
"""Migrate

Util to list and run migrations in the migrations directory.

Usage:
    migrate.py list
    migrate.py run <migration> [-v | --verbose] [-d | --debug]
    migrate.py --version
    migrate.py (-h | --help)

Options:
    --help -h          Show this
    --debug -d         Start the service in debug mode
    --verbose -v       Log to the console along with default files
"""
import logging
import os
import importlib
import inspect
from docopt import docopt

import config.config as c

from utils.mass_updater import MassUpdater


logger = logging.getLogger(c.general.logName+".migrate")

migrations_dir = 'migrations'

migrations = {}


def filter_files(f):
    if f[-3:] == '.py' and f != "__init__.py":
        return True

    return False


def walk_migrations():
    files = os.listdir(migrations_dir)
    files = filter(filter_files, files)


    for f in files:
        name = migrations_dir + '.' + f[:-3] # Strip the .py and make the module name string
        module = importlib.import_module(name)

        migrations[f[:-3]] = {
            "module": module,
            "description": inspect.getdoc(module)
        }


def list_migrations():
    print "Current migrations:"
    for migration in migrations:
        print "\t{} - {}".format(migration, migrations[migration]['description'])


def run_migrations(migration):
    for model in migration['module'].models:
        run_migration(model, migration['module'].migration)


def run_migration(model, migration):
    mu = MassUpdater(model, migration)
    mu.start_migration()


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug v2.0.0')
    walk_migrations()

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

    if arguments['run']:
        migration = arguments['<migration>']

        if migration in migrations:
            migration = migrations[migration]

            run_migrations(migration)
