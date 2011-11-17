from django.contrib.admin.sites import AdminSite as DjangoAdminSite

from .views.search import GenericKeyFacetsMixin
from .views.search import ModelPreviewMixin
from .views.search import ModelSearchBackfillMixin
from .views.search import TypeAndModelQueryMixin

# TODO: Remove these when we reach version 2.0, these are here to maintain
#       backwards compatibility.
from .views.search import EXCLUDED_MODELS_FROM_FACETS
from .views.search import EXCLUDED_APPS_FROM_FACETS


class AdminSite(GenericKeyFacetsMixin, ModelSearchBackfillMixin,
        ModelPreviewMixin, TypeAndModelQueryMixin, DjangoAdminSite):
    pass


site = AdminSite()
