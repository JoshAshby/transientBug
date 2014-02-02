import os
from fabric.api import run, env, cd, prefix
from contextlib import contextmanager as _contextmanager


if env.host == "localhost":
    path = os.path.abspath(__file__).rsplit('/', 1)[0]
    venv = path + "/virt/{}/bin/activate".format("package")
    env.static = "/srv/http/transientbug/static/"

else:
    import secrets
    path = secrets.remote_base
    env.key_name = secrets.ssh_key
    venv = path + "/virt/{}/bin/activate".format("normal")
    env.static = secrets.remote_static

env.directory = path + "/app/"
env.activate = 'source '+venv


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def update():
    run("git pull")


def static():
    run("grunt")
    run("cp -r interface/build/* {}".format(env.static))


def start():
    with virtualenv():
        run("python app.py start -d")


def stop():
    with virtualenv():
        run("python app.py stop")


def restart():
    stop()
    start()


def deploy():
    update()
    static()
    restart()
