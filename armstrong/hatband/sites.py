import json

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

        urlpatterns = patterns('',
            url(r"^armstrong/search/facets/$",
                    self.admin_view(self.generic_key_facets),
                    name="generic_key_facets",
                ),
            url(r"^armstrong/search/facet_values/$",
                    self.admin_view(self.generic_key_modelsearch),
                    name="generic_key_modelsearch"
                ),
            url(r"^armstrong/search/type_and_model_to_query/$",
                    self.admin_view(self.type_and_model_to_query),
                    name="type_and_model_to_query",
                ),
            url(r"^armstrong/render_model_preview/$",
                    self.admin_view(self.render_model_preview),
                    name="render_model_preview"
                )
        )
        
        model_urls = []
        for model, model_admin in self._registry.iteritems():
            model_urls.append(
                    url(r"^%s/%s/search/$" % (
                            model._meta.app_label,
                            model._meta.module_name),
                    self.admin_view(self.generic_key_modelsearch),
                    kwargs={'app_label': model._meta.app_label,
                            'model_name': model._meta.module_name},
                    name="%s_%s_search" % (
                            model._meta.app_label,
                            model._meta.module_name))
                )

        urlpatterns += patterns('', *model_urls)

        return urlpatterns + super(AdminSite, self).get_urls()

    @json_response
    def generic_key_facets(self, request):
        """Find all available facets/Models for VisualSearch"""

        excluded_apps = Q(app_label__in=EXCLUDED_APPS_FROM_FACETS)
        excluded_models = Q()
        for app_label, model in EXCLUDED_MODELS_FROM_FACETS:
            excluded_models = excluded_models | Q(app_label=app_label,
                    model=model)
        values = "model", "app_label", "id"
        content_types = ContentType.objects.values_list(*values) \
                .exclude(excluded_apps | excluded_models)
        return dict([(str(a), {"app_label": str(b), "id": str(c)}) for a, b, c in content_types])

    def type_and_model_to_query(self, request):
        """
        Return JSON for an individual Model instance

        If the required parameters are wrong, return 400 Bad Request
        If the parameters are correct but there is no data, return empty JSON

        """
        try:
            ctype = ContentType.objects.get(pk=request.GET.get("content_type_id"))
        except ContentType.DoesNotExist:
            return HttpResponseBadRequest()

        try:
            model = ctype.model_class()
            result = model.objects.get(pk=request.GET["object_id"])
        except KeyError:
            return HttpResponseBadRequest()
        except model.DoesNotExist:
            data = ""
        else:
            data = '%s: "%d: %s"' % (ctype.model, result.pk, result)

        return HttpResponse(json.dumps({"query": data}))

    def generic_key_modelsearch(self, request, app_label=None, model_name=None):
        """
        Find instances for the requested model and return them as JSON.
        # TODO: add test coverage for this

        """
        if not (app_label and model_name):
            try:
                app_label = request.GET['app_label']
                model_name = request.GET['model_name']
            except KeyError:
                return HttpResponseBadRequest()

            # Django ChangeList.get_query_set() will cry on unexpected GET params
            mutable = request.GET.copy()
            mutable.pop('app_label')
            mutable.pop('model_name')
            request.GET = mutable

        try:
            ctype = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            return HttpResponseBadRequest()

        model = ctype.model_class()
        model_admin = self._registry[model].__class__(model, self)
        model_admin.change_list_template = "admin/hatband/change_list.json"
        return model_admin.changelist_view(request)

    def render_model_preview(self, request):
        type = ContentType.objects.get(pk=request.GET["content_type"])
        model = type.model_class().objects.get(pk=request.GET["object_id"])
        template = request.GET.get("template", "preview")
        return HttpResponse(render_model(model, template))


site = AdminSite()
