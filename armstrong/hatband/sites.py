from django.conf import settings
from django.contrib.admin.sites import AdminSite as DjangoAdminSite
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest

from .contextmanagers import preserve_attr
from .decorators import json_response

from armstrong.core.arm_layout.utils import render_model


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

        search = [
            url(r"^armstrong/search/facets/$",
                    self.admin_view(self.generic_key_facets),
                    name="generic_key_facets",
                ),
            url(r"^armstrong/search/type_and_model_to_query/$",
                    self.admin_view(self.type_and_model_to_query),
                    name="type_and_model_to_query",
                ),
            # an unusable base URL for reversing
            url(r"^armstrong/search/$",
                    self.admin_view(lambda request: HttpResponseBadRequest()),
                    name="generic_key_modelsearch",
                ),
            url(r"^armstrong/search/(?P<app_label>\w+)/(?P<model_name>\w+)/$",
                    self.admin_view(self.generic_key_modelsearch),
                    name="generic_key_modelsearch"
                ),
            url(r"^armstrong/render_model_preview/$",
                    self.admin_view(self.render_model_preview),
                    name="render_model_preview"
                )
        ]
        
        urlpatterns = patterns('', *search)

        return urlpatterns + super(AdminSite, self).get_urls()

    @json_response
    def generic_key_facets(self, request):
        excluded_apps = Q(app_label__in=EXCLUDED_APPS_FROM_FACETS)
        excluded_models = Q()
        for app_label, model in EXCLUDED_MODELS_FROM_FACETS:
            excluded_models = excluded_models | Q(app_label=app_label,
                    model=model)
        values = "model", "app_label", "id"
        content_types = ContentType.objects.values_list(*values) \
                .exclude(excluded_apps | excluded_models)
        return dict([(str(a), {"app_label": str(b), "id": str(c)}) for a, b, c in content_types])

    @json_response
    def type_and_model_to_query(self, request):
        # TODO: handle error 404 error state
        # TODO: handle invalid request error state
        type = ContentType.objects.get(pk=request.GET["content_type_id"])
        model = type.model_class().objects.get(pk=request.GET["object_id"])
        return {"query": '%s: "%d: %s"' % (type.model, model.pk, str(model))}

    def generic_key_modelsearch(self, request, app_label, model_name):
        # TODO: deal with missing/bad requests
        # TODO: add test coverage for this
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model  = content_type.model_class()
        model_admin = self._registry[model].__class__(model, self)
        model_admin.change_list_template = "admin/hatband/change_list.json"
        return model_admin.changelist_view(request)

    def render_model_preview(self, request):
        type = ContentType.objects.get(pk=request.GET["content_type"])
        model = type.model_class().objects.get(pk=request.GET["object_id"])
        template = request.GET.get("template", "preview")
        return HttpResponse(render_model(model, template))


site = AdminSite()
