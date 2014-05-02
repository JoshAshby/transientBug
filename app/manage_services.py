#!/usr/bin/env python2
"""transientBug v2.0.0

Usage:
  manage_services.py (start | stop | restart) <service> [-d | --no-daemon] [-v | --verbose]
  manage_services.py --version
  manage_services.py (-h | --help)


Options:
  --help -h          Show this
  --no-daemon -d     Start the service but don't fork to the background
  --verbose -v       Log to the console too (doesn't do anything right now)

"""
from config.rough import rough_parse_config, setup_log
from daemons.simpleDaemon import Daemon
from docopt import docopt


def run_main_server(self):
    setup_log()
    import utils.framework as fw
    fw.init()
    __import__("controllers.controllerMap", globals(), locals())
    fw.server()


def run_downloader(self):
    setup_log("downloader")
    from daemons.downloader.downloader import Downloader

    worker = Downloader()
    worker.start()


def run_emailer(self):
    setup_log("emailer")
    from daemons.emailer.emailer import Emailer

    worker = Emailer()
    worker.start()


daemons = {
    "main-server": run_main_server,
    "downloader": run_downloader,
    "emailer": run_emailer
}


if __name__ == "__main__":
    arguments = docopt(__doc__, version='transientBug v2.0.0')

    run = daemons[arguments["<service>"]]
    config = rough_parse_config(arguments["<service>"])

    if not arguments["--no-daemon"] or arguments["stop"] or arguments["restart"]:
        AppDaemon = type('AppDaemon', (Daemon,), {"run": run})
        app = AppDaemon(config["files"]["pid"], stderr=config["files"]["stderr"])

    else:
        App = type('App', (), {"start": run})
        app = App()

    if arguments["start"]:
        app.start()

    if arguments["stop"]:
        app.stop()

    if arguments["restart"]:
        app.restart()
