from django.conf import settings
from django.contrib.admin.sites import AdminSite as DjangoAdminSite
from django.contrib.admin.sites import site as django_site
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
import json


def json_response(func):
    def inner(*args, **kwargs):
        data = func(*args, **kwargs)
        return HttpResponse(json.dumps(data))
    return inner

EXCLUDED_MODELS_FROM_FACETS = getattr(settings,
    "ARMSTRONG_EXCLUDED_MODELS_FROM_FACETS", [
        ("arm_wells", "welltype"),
        ("arm_wells", "well"), # remove this if we decide to support this
    ])

EXCLUDED_APPS_FROM_FACETS = getattr(settings,
    "ARMSTRONG_EXCLUDED_APPS_FROM_FACETS", [
        "admin", "auth", "contenttype", "reversion", "sessions", "sites",
    ])

class AdminSite(DjangoAdminSite):
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        return patterns('',
            url(r"^armstrong/search/generickey/facets/$", self.generic_key_facets, name="generic_key_facets"),
        ) + super(AdminSite, self).get_urls()

    @json_response
    def generic_key_facets(self, request):
        excluded_apps = Q(app_label__in=EXCLUDED_APPS_FROM_FACETS)
        excluded_models = Q()
        for app_label, model in EXCLUDED_MODELS_FROM_FACETS:
            excluded_models = excluded_models | Q(app_label=app_label,
                    model=model)
        content_types = ContentType.objects.values_list("model", flat=True) \
            .exclude(excluded_apps | excluded_models)
        return [str(a) for a in content_types]


site = AdminSite()
