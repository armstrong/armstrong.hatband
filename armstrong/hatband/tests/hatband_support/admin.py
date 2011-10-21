from armstrong import hatband
from . import models
from django.db.models import TextField
from django.forms.widgets import TextInput


class ArticleAdmin(hatband.ModelAdmin):

    class Meta:
        model = models.TestArticle


class ArticleOverrideAdmin(hatband.ModelAdmin):

    formfield_overrides = {
        TextField: {'widget': TextInput},
    }

    class Meta:
        model = models.TestArticle


class ArticleTabularInline(hatband.TabularInline):

    class Meta:
        model = models.TestArticle


class ArticleStackedInline(hatband.StackedInline):

    class Meta:
        model = models.TestArticle


class CategoryAdminTabbed(hatband.ModelAdmin):

    inlines = ArticleTabularInline

    class Meta:
        model = models.TestCategory


class CategoryAdminStacked(hatband.ModelAdmin):

    inlines = ArticleStackedInline

    class Meta:
        model = models.TestCategory
