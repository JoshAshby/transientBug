import secrets
from fabric.api import run, env, cd, prefix
from contextlib import contextmanager as _contextmanager

path = secrets.remote_base
env.key_name = secrets.ssh_key
venv = path + "/virt/{}/bin/activate".format("normal")
env.static = secrets.remote_static
env.hosts = ["transientbug.com"]
env.path = path
env.directory = path + "/app/"
env.activate = 'source '+venv


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def update():
    with cd(env.path):
        run("git pull")


def static():
    with cd(env.path):
        run("grunt")
        run("cp -r interface/build/* {}".format(env.static))


def start():
    with virtualenv():
        run("supervisorctl start all")


def stop():
    with virtualenv():
        run("supervisorctl stop all")


def restart():
    with virtualenv():
        run("supervisorctl restart all")


def deploy():
    stop()
    update()
    static()
    start()
