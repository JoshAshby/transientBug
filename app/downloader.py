#!/usr/bin/env python2
"""TransientBug Downloader Daemon

Usage:
  downloader.py start [-d | --daemon]
  downloader.py stop
  downloader.py restart
  downloader.py --version
  downloader.py (-h | --help)

Options:
  --help -h      Show this
  --daemon -d    Start the downloader as a daemon

"""
from config.rough import rough_parse_config, setup_log
from daemons.simpleDaemon import Daemon
from docopt import docopt


def run(self):
    setup_log("downloader")
    from daemons.downloader.downloader import Downloader

    downloader = Downloader()
    downloader.start()


if __name__ == "__main__":
    config = rough_parse_config("downloader")
    arguments = docopt(__doc__, version='TransientBug Downloader Daemon v0.1.0')

    if arguments["--daemon"] or arguments["stop"] or arguments["restart"]:
        AppDaemon = type('AppDaemon', (Daemon,), {"run": run})
        app = AppDaemon(config["files"]["pid"], stderr=config["files"]["stderr"])
    else:
        App = type('App', (), {"run": run})
        app = App()

    if arguments["start"]:
        if not arguments["--daemon"]:
            app.run()
        else:
            app.start()

    if arguments["stop"]:
        app.stop()

    if arguments["restart"]:
        app.restart()
