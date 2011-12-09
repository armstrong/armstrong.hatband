from armstrong.core.arm_layout.utils import render_model
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from ..http import JsonResponse

EXCLUDED_MODELS_FROM_FACETS = getattr(settings,
    "ARMSTRONG_EXCLUDED_MODELS_FROM_FACETS", [
        ("arm_wells", "welltype"),

        # remove this next line if we decide to support this
        ("arm_wells", "well"),
    ])

EXCLUDED_APPS_FROM_FACETS = getattr(settings,
    "ARMSTRONG_EXCLUDED_APPS_FROM_FACETS", [
        "admin", "auth", "contenttype", "reversion", "sessions", "sites",
    ])


class ArmstrongBaseMixin(object):
    url_prefix = "armstrong"


class GenericKeyFacetsMixin(ArmstrongBaseMixin):
    url = "search/generickey/facets/"

    def get_urls(self):
        urlpatterns = patterns('',
            url(r"^%s/%s$" % (self.url_prefix, self.url),
                self.admin_view(self.generic_key_facets),
                name="generic_key_facets",
            )
        )
        return urlpatterns + super(GenericKeyFacetsMixin, self).get_urls()

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
        return JsonResponse(dict([(str(a), {"app_label": str(b), "id": str(c)})
                for a, b, c in content_types]))


class ModelSearchBackfillMixin(object):
    slug = "search"
    view_name_template = "%s_%s_search"

    def get_urls(self):
        # TODO: Attempt
        model_urls = []
        for model, model_admin in self._registry.iteritems():
            model_urls.append(
                    url(r"^%s/%s/%s/$" % (
                            model._meta.app_label,
                            model._meta.module_name,
                            self.slug),
                    self.admin_view(self.generic_key_modelsearch),
                    kwargs={'app_label': model._meta.app_label,
                            'model_name': model._meta.module_name},
                    name=self.view_name_template % (
                            model._meta.app_label,
                            model._meta.module_name))
                )

        return patterns('', *model_urls) \
                + super(ModelSearchBackfillMixin, self).get_urls()

    def generic_key_modelsearch(self, request, app_label, model_name):
        """
        Find instances for the requested model and return them as JSON.
        # TODO: add test coverage for this
        """
        content_type = ContentType.objects.get(app_label=app_label,
                model=model_name)

        model = content_type.model_class()
        model_admin = self._registry[model].__class__(model, self)
        model_admin.change_list_template = "admin/hatband/change_list.json"
        return model_admin.changelist_view(request)


class ModelPreviewMixin(ArmstrongBaseMixin):
    """
    Provides a way to render a model's preview display
    """
    slug = "render_model_preview"

    def get_urls(self):
        urlpatterns = patterns('',
            url(r"^%s/%s/$" % (self.url_prefix, self.slug),
                self.admin_view(self.render_model_preview),
                name="render_model_preview"
            )
        )
        return urlpatterns + super(ModelPreviewMixin, self).get_urls()

    def render_model_preview(self, request):
        type = ContentType.objects.get(pk=request.GET["content_type"])
        model = type.model_class().objects.get(pk=request.GET["object_id"])
        template = request.GET.get("template", "preview")
        return HttpResponse(render_model(model, template))


class TypeAndModelQueryMixin(ArmstrongBaseMixin):
    type_and_model_to_query_url = "search/type_and_model_to_query/"

    def get_urls(self):
        urlpatterns = patterns('',
            url(r"^%s/%s$" % (self.url_prefix,
                              self.type_and_model_to_query_url),
                self.admin_view(self.type_and_model_to_query),
                name="type_and_model_to_query",
            )
        )
        return urlpatterns + super(TypeAndModelQueryMixin, self).get_urls()

    def type_and_model_to_query(self, request):
        """
        Return JSON for an individual Model instance

        If the required parameters are wrong, return 400 Bad Request
        If the parameters are correct but there is no data, return empty JSON

        """
        try:
            content_type = ContentType.objects.get(
                    pk=request.GET.get("content_type_id"))
        except ContentType.DoesNotExist:
            return HttpResponseBadRequest()

        try:
            model = content_type.model_class()
            result = model.objects.get(pk=request.GET["object_id"])
        except KeyError:
            return HttpResponseBadRequest()
        except model.DoesNotExist:
            data = ""
        else:
            data = '%s: "%d: %s"' % (content_type.model, result.pk, result)

        return JsonResponse({"query": data})
