from armstrong.dev.tests.utils import ArmstrongTestCase
from django.utils import unittest


class HatbandTestCase(ArmstrongTestCase):
    pass


class HatbandTestMixin(object):

    script_code = """
    <script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>
    """.strip()
    textarea_code = 'class="ckeditor"></textarea>'

    def assertCkEditorPresent(self, response):
        self.assertContains(response, self.script_code)
        self.assertContains(response, self.textarea_code)

    def assertCkEditorNotPresent(self, response):
        self.assertNotContains(response, self.script_code)
        self.assertNotContains(response, self.textarea_code)
