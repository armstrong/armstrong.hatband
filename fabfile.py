from armstrong.dev.tasks import *

settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'armstrong.hatband',
        'armstrong.hatband.tests.hatband_support',
        'lettuce.django',
    ),
    'STATIC_URL': '/TESTING/',
}

main_app = "hatband"
tested_apps = ("hatband_support", "hatband", )
full_name = "armstrong.hatband"
pip_install_first = True

