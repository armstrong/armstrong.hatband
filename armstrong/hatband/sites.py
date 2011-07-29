from contextlib import contextmanager
from django.conf import settings
from django.contrib.admin.sites import AdminSite as DjangoAdminSite
from django.contrib.admin.sites import site as django_site
from django.contrib.admin.views.main import ChangeList as DjangoChangeList
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


# TODO: find a home for this
@contextmanager
def preserve_attr(obj, attr):
    original = getattr(obj, attr)
    yield
    setattr(obj, attr, original)


class AdminSite(DjangoAdminSite):
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        search = [
            url(r"^armstrong/search/generickey/facets/$",
                self.generic_key_facets, name="generic_key_facets"),
        ]
        for model, model_admin in self._registry.iteritems():
            search.append(
                    url(r"^(?P<app_label>%s)/(?P<model_name>%s)/search/" % (
                        model._meta.app_label, model._meta.module_name),
                    self.generic_key_modelsearch, name="%s_%s_search" % (
                        model._meta.app_label, model._meta.module_name)))

        urlpatterns = patterns('', *search)
        print urlpatterns
        return urlpatterns + super(AdminSite, self).get_urls()

    @json_response
    def generic_key_facets(self, request):
        excluded_apps = Q(app_label__in=EXCLUDED_APPS_FROM_FACETS)
        excluded_models = Q()
        for app_label, model in EXCLUDED_MODELS_FROM_FACETS:
            excluded_models = excluded_models | Q(app_label=app_label,
                    model=model)
        content_types = ContentType.objects.values_list("model", "app_label") \
                .exclude(excluded_apps | excluded_models)
        return dict([(str(a), str(b)) for a, b in content_types])

    def generic_key_modelsearch(self, request, app_label, model_name):
        # TODO: deal with missing/bad requests
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model  = content_type.model_class()
        model_admin = self._registry[model]
        with preserve_attr(model_admin, "change_list_template"):
            model_admin.change_list_template = "admin/hatband/change_list.json"
            return model_admin.changelist_view(request)


site = AdminSite()
