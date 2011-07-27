from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from . import widgets

RICH_TEXT_DBFIELD_OVERRIDES = {
    models.TextField: {'widget': widgets.RichTextWidget},
}


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


class StackedInline(admin.StackedInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


class TabularInline(admin.TabularInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


# TODO: move this over to somewhere more appropriate
def static_url(url):
    return ''.join((settings.STATIC_URL, url))


class GenericKeyWidget(forms.Widget):
    template = "admin/hatband/widgets/generickey.html"

    class Media:
        js = (static_url("visualsearch/dependencies.js"),
              static_url("visualsearch/visualsearch.js"),
              static_url("generickey.js"),
             )

        css = {
            "all": (static_url("visualsearch/visualsearch.css"), ),
        }


    def __init__(self, *args, **kwargs):
        super(GenericKeyWidget, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        widget_id = id(self)
        return render_to_string(self.template, {"widget_id": widget_id, })

class DeletionWidget(forms.CheckboxInput):
    pass


class OrderableGenericKeyLookupForm(forms.ModelForm):
    class Meta:
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_id": GenericKeyWidget(),
            "order": forms.HiddenInput(),
        }


class GenericKeyInline(InlineModelAdmin):
    form = OrderableGenericKeyLookupForm
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES
    template = "admin/edit_inline/generickey.html"
