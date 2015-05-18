from invoke import task, run
from armstrong.dev.tasks import *


@task
def update_visualsearch():
    run("cp -R ./vendor/visualsearch/build-min/* ./armstrong/hatband/static/visualsearch/")
    run("cp ./vendor/visualsearch/lib/images/embed/icons/* ./armstrong/hatband/static/images/embed/icons/")
