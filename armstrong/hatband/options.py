from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django import forms
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


class OrderableGenericKeyLookupForm(forms.ModelForm):
    class Meta:
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_id": widgets.GenericKeyWidget(),
            "order": forms.HiddenInput(),
        }


class GenericKeyInline(InlineModelAdmin):
    form = OrderableGenericKeyLookupForm
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES
    template = "admin/edit_inline/generickey.html"
