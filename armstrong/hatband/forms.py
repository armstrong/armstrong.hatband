from django import forms
from django.db import models

from . import widgets

RICH_TEXT_DBFIELD_OVERRIDES = {
    models.TextField: {'widget': widgets.RichTextWidget},
}


class OrderableGenericKeyLookupForm(forms.ModelForm):
    class Meta:
        widgets = {
            "content_type": forms.HiddenInput(),
            "object_id": widgets.GenericKeyWidget(),
            "order": forms.HiddenInput(),
        }
