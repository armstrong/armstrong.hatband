from armstrong.dev.tasks import *

settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'armstrong.admin2',
        'armstrong.admin2.tests.admin2_support',
        'lettuce.django',
    ),
}

main_app = "admin2"
tested_apps = ("admin2_support", "admin2", )
full_name = "armstrong.admin2"
pip_install_first = True
