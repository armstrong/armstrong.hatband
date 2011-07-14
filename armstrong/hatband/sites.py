from django.contrib.admin.sites import AdminSite as DjangoAdminSite
from django.contrib.admin.sites import site as django_site


class HatbandAndDjangoRegistry(object):
    def __init__(self, site, default_site=None):
        if default_site is None:
            default_site = django_site
        super(HatbandAndDjangoRegistry, self).__init__()
        self._site = site
        self._registry = {}
        self.dicts = [self._registry, default_site._registry]

    def items(self):
        for d in self.dicts:
            for item in d.items():
                yield item

    def iteritems(self):
        return iter(self.items())

    def __contains__(self, k):
        for d in self.dicts:
            if k in d:
                return True
        return False


class AdminSite(DjangoAdminSite):
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        return patterns('',
            # Custom hatband Views here
        ) + super(AdminSite, self).get_urls()


site = AdminSite()
site._registry = HatbandAndDjangoRegistry(site, default_site=django_site)
