from django.forms import widgets
from django.conf import settings
try:
    from django.contrib.staticfiles.templatetags.staticfiles import static
except ImportError:  # DROP_WITH_DJANGO13
    if not getattr(settings, "STATIC_URL"):
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "You're using static files without STATIC_URL in settings.")

    def static(url):
        return ''.join((settings.STATIC_URL, url))


class CKEditorWidget(widgets.Textarea):
    class Media:
        js = (static("ckeditor/ckeditor.js"),)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'ckeditor'}
        if attrs is not None:
            final_attrs.update(attrs)
            if 'class' in attrs:
                final_attrs['class'] = ' '.join((attrs['class'], 'ckeditor'))
        super(CKEditorWidget, self).__init__(attrs=final_attrs)
