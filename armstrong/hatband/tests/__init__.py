from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from contextlib import contextmanager
import fudge

from .http import *
from .sites import *
from .widgets import *

from ... import hatband


def generate_random_registry():
    from ._utils import random_range
    return dict([("key%d" % i, i) for i in random_range()])


@contextmanager
def fake_autodiscover():
    from django.contrib import admin
    autodiscover = fudge.Fake().is_callable()
    with fudge.patched_context(admin, "autodiscover", autodiscover):
        yield

@contextmanager
def fake_django_site_registry(test):
    with fake_autodiscover():
        random_registry = generate_random_registry()
        from django.contrib import admin
        site = fudge.Fake()
        site.has_attr(_registry=random_registry)
        with fudge.patched_context(admin, "site", site):
            test.assertEqual( len(random_registry.items()),
                    len(site._registry.items()), msg="sanity check")
            yield random_registry


class AutodiscoverTestCase(HatbandTestCase):
    def setUp(self):
        from copy import copy
        self.original_site = copy(hatband.site)
        hatband.site._registry = {}

    def tearDown(self):
        hatband.site = self.original_site

    @fudge.test
    def test_dispatches_to_djangos_autodiscover(self):
        from django.contrib import admin
        autodiscover = fudge.Fake().is_callable().expects_call()

        with fudge.patched_context(admin, "autodiscover", autodiscover):
            hatband.autodiscover()


    @fudge.test
    def test_has_a_copy_of_main_django_registry(self):
        random_registry = generate_random_registry()

        from django.contrib import admin
        site = fudge.Fake()
        site.has_attr(_registry=random_registry)

        with fake_autodiscover():
            with fudge.patched_context(admin, "site", site):
                hatband.autodiscover()
                for key in random_registry.keys():
                    self.assertTrue(key in hatband.site._registry)


    @fudge.test
    def test_has_hatband_registered_plus_(self):
        with fake_django_site_registry(self) as random_registry:
            from .hatband_support.models import TestCategory

            self.assertFalse(TestCategory in hatband.site._registry.keys(),
                    msg="Sanity check")
            hatband.site.register(TestCategory)
            self.assertTrue(TestCategory in hatband.site._registry.keys(),
                    msg="Sanity check")

            hatband.autodiscover()
            registry = hatband.site._registry.items()
            self.assertTrue(TestCategory in hatband.site._registry.keys(),
                    msg="TestCategory should still be in the registry")

    @fudge.test
    def test_original_django_sites_registry_remains_untouched(self):
        with fake_django_site_registry(self) as random_registry:
            from .hatband_support.models import TestCategory
            self.assertFalse(TestCategory in random_registry.keys())
            hatband.site.register(TestCategory)
            hatband.autodiscover()

            self.assertFalse(TestCategory in random_registry.keys())
