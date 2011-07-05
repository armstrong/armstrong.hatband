from .._utils import *
from ...widgets import CKEditorWidget, RichTextWidget
from django.forms.widgets import Textarea
from django.conf import settings

TEST_SETTINGS = {
    "ARMSTRONG_HATBAND_RICHTEXTEDITOR": "django.forms.widgets.Textarea",
}


class RichTextFieldTestCase(HatbandTestCase):

    def test_default(self):
        ckeditor = CKEditorWidget()
        widget = RichTextWidget()
        ckeditor_out = str(ckeditor.render('widget', ''))
        widget_out = str(widget.render('widget', ''))
        self.assertEquals(ckeditor_out, widget_out)

    def test_non_default_setting(self):
        with self.settings(**TEST_SETTINGS):
            textarea = Textarea()
            widget = RichTextWidget()
            textarea_out = str(textarea.render('widget', ''))
            widget_out = str(widget.render('widget', ''))
            self.assertEquals(textarea_out, widget_out)

    def test_kwargs_passthrough(self):
        attrs = {'cols': 50, 'class': 'something'}
        ckeditor = CKEditorWidget(attrs=attrs)
        widget = RichTextWidget(attrs=attrs)
        ckeditor_out = str(ckeditor.render('widget', ''))
        widget_out = str(widget.render('widget', ''))
        self.assertEquals(ckeditor_out, widget_out)
