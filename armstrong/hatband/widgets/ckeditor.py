from django.forms import widgets

class CKEditorWidget(widgets.Textarea):
    
    def __init__(self, attrs=None):
        final_attrs = {'class': 'ckEditor'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(CKEditorWidget, self).__init__(attrs=final_attrs)
    pass