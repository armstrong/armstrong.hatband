from django.contrib import admin
from django.db import models
from armstrong.hatband import widgets

RICH_TEXT_DBFIELD_OVERRIDES = {
    models.TextField: {'widget': widgets.RichTextWidget},
}

class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES
    
class StackedInline(admin.StackedInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES

class TabularInline(admin.TabularInline):
    formfield_overrides = RICH_TEXT_DBFIELD_OVERRIDES