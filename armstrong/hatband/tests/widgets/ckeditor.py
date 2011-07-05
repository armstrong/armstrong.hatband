from django.conf import settings
from .._utils import *
from ...widgets import CKEditorWidget


class CKEditorTestCase(HatbandTestCase):

    def test_render(self):
        widget = CKEditorWidget()
        htmlout = str(widget.render('widget', ''))
        self.assertTrue('class="ckeditor"' in htmlout)

    def test_render_with_additional_classes(self):
        widget = CKEditorWidget(attrs={'class': 'something'})
        htmlout = widget.render('widget', '')
        self.assertTrue('class="something ckeditor"' in htmlout)
