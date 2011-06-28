from armstrong.dev.tasks import *

settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'armstrong.hatband',
        'armstrong.hatband.tests.admin2_support',
        'lettuce.django',
    ),
}

main_app = "hatband"
tested_apps = ("hatband_support", "hatband", )
full_name = "armstrong.hatband"
pip_install_first = True
