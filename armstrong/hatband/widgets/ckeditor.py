from django.forms import widgets
from django.conf import settings


class CKEditorWidget(widgets.Textarea):

    class Media:
        js = (''.join((settings.STATIC_URL, "ckeditor/ckeditor.js")),)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'ckeditor'}
        if attrs is not None:
            final_attrs.update(attrs)
            if 'class' in attrs:
                final_attrs['class'] = ' '.join((attrs['class'], 'ckeditor'))
        super(CKEditorWidget, self).__init__(attrs=final_attrs)
