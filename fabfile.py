from fabric.api import env
from fabric.decorators import task
from fabric.context_managers import cd, prefix, warn_only
from fabric.operations import run, local, get, put, prompt

from fabric.colors import red, green, blue, yellow, white, magenta, cyan

from contextlib import contextmanager as _contextmanager
from app.utils.standard import StandardODM
import yaml
import arrow

config = None
with open("fabconfig.yaml", "r") as f:
    config = StandardODM(**yaml.load(f.read()))

if not config:
    raise Exception("Failed to load fabconfig.yaml!")


env.key_name = config.ssh_key
env.hosts = config.hosts
env.path = config.path


@_contextmanager
def virtualenv(virt=config.virtualenv_name):
    with cd(env.path):
        with prefix("source {}/virt/{}/bin/activate".format(env.path, virt)):
            yield


def get_service(action):
    ans = prompt(cyan("What services do you want to {}? (Case sensitive, space separated or `all` or `none`)".format(action)))

    if ans and not ans.lower() == "none":
        return ans

    return None

def services(action, ans):
    actions = {
        "restart": "Restarting",
        "start": "Starting",
        "stop": "Stopping"
    }
    print cyan("{} services [{}]...".format(actions[action], ans))
    with cd(env.path), virtualenv():
        with cd("app/"):
            run("supervisorctl {} {}".format(action, ans))

@task
def static():
    print cyan("Rebuilding static files...")
    with cd(env.path):
        run("grunt")
        run("cp -r interface/build/* {}/static/".format(config.html))

@task
def git_pull():
    print cyan("Updating git repository...")
    with cd(env.path):
        run("git pull origin master")

@task
def status():
    with cd(env.path), virtualenv():
        with cd("app/"):
            run("supervisorctl status")

@task
def restart():
    status()
    ans = get_service("restart")
    if ans is not None:
        services("restart", ans)

@task
def start():
    status()
    ans = get_service("start")
    if ans is not None:
        services("start", ans)

@task
def stop():
    status()
    ans = get_service("stop")
    if ans is not None:
        services("stop", ans)

@task
def backup():
    time = arrow.utcnow().format("YYYY-MM-DD_HH-mm-ss")
    db_backup = "transientbug_rethinkdb_backup_{}.tar.gz".format(time)
    html_backup = "transientbug_html_backup_{}.tar.gz".format(time)
    with cd(env.path), virtualenv():
        run("rethinkdb dump {}".format(db_backup))
        run("tar -cvpzf {} {}".format(html_backup, config.html))
        get(db_backup)
        get(html_backup)
