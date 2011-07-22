from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# Make this a drop-in replacement for Django's built-in Admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import HORIZONTAL, VERTICAL

# Below are overrides that we provide that are Hatband specific
from .options import ModelAdmin, StackedInline, TabularInline
from armstrong.hatband.sites import AdminSite, site


def autodiscover():
    """
    TODO: document
    """
    from django.contrib.admin import autodiscover as django_autodiscover
    django_autodiscover()

    from copy import copy
    from django.contrib.admin import site as django_site
    registry = copy(django_site._registry)
    registry.update(site._registry)
    site._registry = registry
