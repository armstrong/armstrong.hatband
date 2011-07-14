from django.contrib.admin.sites import AdminSite as DjangoAdminSite
from django.contrib.admin.sites import site as django_site


class AdminSite(DjangoAdminSite):
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        return patterns('',
            # Custom hatband Views here
        ) + super(AdminSite, self).get_urls()


site = AdminSite()
site._registry = django_site._registry
