from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# Make this a drop-in replacement for Django's built-in Admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import HORIZONTAL, VERTICAL

# Below are overrides that we provide that are Hatband specific
from .options import ModelAdmin, StackedInline, TabularInline
from armstrong.hatband.sites import AdminSite, site


# This is copied directly from Django as there is no way to specify what `site`
# object you want to use inside `autodiscover`.  This is important for Hatband,
# as all of Armstrong will eventually use `from armstrong import hatband as
# admin` and us Hatband's `site` value.
#
# TODO: keep this in sync with django.contrib.admin.autodiscover (ongoing)
def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.

    .. _warning: This is a direct copy and paste from ``django.contrib.admin``
                 becuase they do not support providing a different ``site``
                 than their own.
    """

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.admin' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'admin'):
                raise
