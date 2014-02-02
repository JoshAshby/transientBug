#!/usr/bin/env python
"""

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import subprocess

base = os.path.realpath(__file__).rsplit("/", 1)[0]

BOOTSTRAP_FOLDER = "bootstrap"
bootstrap = []

ignore_folders = ["helpers"]
ignore_files = ["variables"]

for top, folders, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
  folder = top.split(base)[1].strip("/")

  if folder == BOOTSTRAP_FOLDER:
      for name in bootstrap:
          name = BOOTSTRAP_FOLDER+"/"+name
          path = os.path.realpath(name+".less")

          print "Compiling bootstrap theme {theme}.less to ../css/{theme}.css".format(theme=name)

          subprocess.call("lessc {path} > ../css/{name}.css".format(name=name, path=path), shell=True)

  elif folder in ignore_folders:
      pass

  else:
      for filename in files:
        if filename[0] not in ["~", "."]:
          name, extension = filename.split(".", 1)

          if extension == "less" and name not in ignore_files:
            if folder:
                path = os.path.realpath("/".join([folder, filename]))
                name = "/".join([folder, name])
                print "Compiling {folder}/{filename} to {name}.css".format(name=name, filename=filename, folder=folder)
            else:
                path = os.path.realpath(filename)
                print "Compiling {filename} to {name}.css".format(name=name, filename=filename, folder=folder)
            subprocess.call("lessc {path} > ../css/{name}.css".format(name=name, path=path), shell=True)
