from armstrong import hatband
from hatband_support import models
from django.forms.widgets import TextInput


class ArticleAdmin(hatband.ModelAdmin):

    class Meta:
        model = models.TestArticle


class ArticleOverrideAdmin(hatband.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }

    class Meta:
        model = models.TestArticle


class ArticleTabbedInline(hatband.TabbedInline):

    class Meta:
        model = models.TestArticle


class ArticleStackedInline(hatband.StackedInline):

    class Meta:
        model = models.TestArticle


class CategoryAdminTabbed(hatband.ModelAdmin):

    inlines = ArticleTabbedInline

    class Meta:
        model = models.TestCategory


class CategoryAdminStacked(hatband.ModelAdmin):

    inlines = ArticleStackedInline

    class Meta:
        model = models.TestCategory
