#!/usr/bin/env python2
"""Seshat

Usage:
  app.py start [-d | --daemon]
  app.py stop
  app.py restart
  app.py --version
  app.py (-h | --help)


Options:
  --help -h      Show this
  --daemon -d    Start Seshat as a daemon

"""
import sys
import os
import yaml

from docopt import docopt

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
current_path = os.getcwd() + "/"

config = yaml.load(file(current_path+"/config/config.yaml", 'r'))
for key, fi in config["files"].items():
    if fi[0] != "/":
      config["files"][key] = current_path + fi


def setupLog():
    """
    Sets up the main logger for the daemon
    """
    import logging
    import config.config as c
    level = logging.WARNING
    if c.general.debug:
            level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger(c.general.logName)
    logger.setLevel(level)

    fh = logging.FileHandler(c.general.dirs["log"] + c.general.files["log"])
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if c.general.debug:
        """
        Make sure we're not in daemon mode if we're logging to console too
        """
        try:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        except:
            pass

    return logger


from utils.simpleDaemon import Daemon
class AppDaemon(Daemon):
    def run(self):
        logger = setupLog()
        import seshat.framework as fw
        __import__("controllers.controllerMap", globals(), locals())

        fw.serveForever()

class AppNoDaemon(object):
    def __init__(self):
        pass

    def start(self):
        logger = setupLog()
        import seshat.framework as fw
        __import__("controllers.controllerMap", globals(), locals())
        fw.serveForever()

    def stop(self):
        pass

    def restart(self):
        pass


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Seshat v0.1.0')

    if arguments["--daemon"]:
        app = AppDaemon(config["files"]["pid"], stderr=config["files"]["stderr"])
    else:
        app = AppNoDaemon()

    if arguments["start"]:
        app.start()

    if arguments["stop"]:
        app.stop()

    if arguments["restart"]:
        app.restart()
