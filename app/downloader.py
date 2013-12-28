#!/usr/bin/env python2
"""TransientBug Downloader Daemon

Usage:
  builder.py start [-d | --daemon]
  builder.py stop
  builder.py restart
  builder.py --version
  builder.py (-h | --help)


Options:
  --help -h      Show this
  --daemon -d    Start the builder as a daemon

"""
import sys
import os
import yaml

from utils.simpleDaemon import Daemon
from docopt import docopt

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
current_path = os.getcwd() + "/"

config = yaml.load(file(current_path+"/config/config.yaml", 'r'))["downloader"]

for directory in config["dirs"]:
    if config["dirs"][directory][0] != "/":
        direct = current_path + config["dirs"][directory]
    else:
        direct = config["dirs"][directory]
    if not os.path.exists(direct):
        os.makedirs(direct)
    config["dirs"][directory] = direct

for fi in config["files"]:
    extension = config["files"][fi].rsplit(".", 1)
    if "pid" in extension:
        config["files"][fi] = config["dirs"]["pid"] + config["files"][fi]
    elif "log" in extension:
        config["files"][fi] = config["dirs"]["log"] + config["files"][fi]


def setupLog():
    """
    Sets up the main logger for the daemon
    """
    import logging
    import config.config as c

    level = logging.WARNING
    if c.debug:
            level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger(c.downloader["log_name"])
    logger.setLevel(level)

    logger_w = logging.getLogger("worker")
    logger_w.setLevel(level)

    fh = logging.FileHandler(c.downloader["files"]["log"])
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger_w.addHandler(fh)

    if c.debug:
        """
        Make sure we're not in daemon mode if we're logging to console too
        """
        try:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
            logger_w.addHandler(ch)
        except:
            pass

    return logger


class App(object):
    def start(self):
        self.run()

    def run(self):
        setupLog()
        from daemons.downloader.downloader import Downloader

        downloader = Downloader()
        downloader.start()


if __name__ == "__main__":
    arguments = docopt(__doc__, version='TransientBug Downloader Daemon v0.1.0')

    if arguments["--daemon"] or arguments["stop"] or arguments["restart"]:
        tmp = type('AppDaemon', (App, Daemon,), {})
        app = tmp(config["files"]["pid"], stderr=config["files"]["stderr"])
    else:
        app = App()

    if arguments["start"]:
        app.start()

    if arguments["stop"]:
        app.stop()

    if arguments["restart"]:
        app.restart()
