from django.db.models import TextField
from django.forms.widgets import TextInput

from armstrong import hatband
from .models import TestArticle, TestCategory


class ArticleAdmin(hatband.ModelAdmin):

    class Meta:
        model = TestArticle


class ArticleOverrideAdmin(hatband.ModelAdmin):

    formfield_overrides = {
        TextField: {'widget': TextInput},
    }

    class Meta:
        model = TestArticle


class ArticleTabularInline(hatband.TabularInline):

    class Meta:
        model = TestArticle


class ArticleStackedInline(hatband.StackedInline):

    class Meta:
        model = TestArticle


class CategoryAdminTabbed(hatband.ModelAdmin):

    inlines = ArticleTabularInline

    class Meta:
        model = TestCategory


class CategoryAdminStacked(hatband.ModelAdmin):

    inlines = ArticleStackedInline

    class Meta:
        model = TestCategory
