from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.utils.safestring import mark_safe

from . import forms


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = forms.RICH_TEXT_DBFIELD_OVERRIDES


class StackedInline(admin.StackedInline):
    formfield_overrides = forms.RICH_TEXT_DBFIELD_OVERRIDES


class TabularInline(admin.TabularInline):
    formfield_overrides = forms.RICH_TEXT_DBFIELD_OVERRIDES


class GenericKeyInline(InlineModelAdmin):
    form = forms.OrderableGenericKeyLookupForm
    formfield_overrides = forms.RICH_TEXT_DBFIELD_OVERRIDES
    template = "admin/edit_inline/generickey.html"


class BackboneInline(InlineModelAdmin):
    form = forms.OrderableGenericKeyLookupForm
    formfield_overrides = forms.RICH_TEXT_DBFIELD_OVERRIDES
    template = "admin/edit_inline/backbone.html"
    extra = 0
