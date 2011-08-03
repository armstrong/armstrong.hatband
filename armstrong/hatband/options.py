from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from . import widgets
from .utils import static_url

RICH_TEXT_DBFIELD_OVERRIDES = {
    models.TextField: {'widget': widgets.RichTextWidget},
}


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


class StackedInline(admin.StackedInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


class TabularInline(admin.TabularInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES


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

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs["value"] = value
        final_attrs["is_templated"] = final_attrs["id"].find("__prefix__") > -1
        return render_to_string(self.template, final_attrs)

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
