#!/usr/bin/env python2
"""TransientBug Emailer Daemon

Usage:
  emailer.py start [-d | --daemon]
  emailer.py stop
  emailer.py restart
  emailer.py --version
  emailer.py (-h | --help)

Options:
  --help -h      Show this
  --daemon -d    Start the emailer as a daemon

"""
from config.rough import rough_parse_config, setup_log
from daemons.simpleDaemon import Daemon
from docopt import docopt


def run(self):
    setup_log("emailer")
    from daemons.emailer.emailer import Emailer

    worker = Emailer()
    worker.start()


if __name__ == "__main__":
    config = rough_parse_config("emailer")
    arguments = docopt(__doc__, version='TransientBug Emailer Daemon v0.1.0')

    if arguments["--daemon"] or arguments["stop"] or arguments["restart"]:
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
