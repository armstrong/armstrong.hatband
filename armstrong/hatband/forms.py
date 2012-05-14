from django import forms
from django.conf import settings
from django.db import models

from . import widgets

RICH_TEXT_DBFIELD_OVERRIDES = {
    models.TextField: {'widget': widgets.RichTextWidget},
}


class BackboneFormMixin(object):
    if getattr(settings, "ARMSTRONG_ADMIN_PROVIDE_STATIC", True):
        class Media:
            js = (
                    'hatband/js/jquery-1.6.2.min.js',
                    'hatband/js/underscore.js',
                    'hatband/js/backbone.js',
                    'hatband/js/backbone-inline-base.js')


class OrderableGenericKeyLookupForm(BackboneFormMixin, forms.ModelForm):
    class Meta:
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_id": widgets.GenericKeyWidget(),
            "order": forms.HiddenInput(),
        }
