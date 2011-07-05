from armstrong.utils.backends import GenericBackend

RICH_TEXT_BACKEND = GenericBackend('ARMSTRONG_HATBAND_RICHTEXTEDITOR',
        defaults="armstrong.hatband.widgets.ckeditor.CKEditorWidget")
#RichTextWidget = RICH_TEXT_BACKEND.get_backend


class RichTextWidget(object):
    def __new__(cls, *args, **kwargs):
        return RICH_TEXT_BACKEND.get_backend(*args, **kwargs)
