from armstrong.dev.tests.utils import ArmstrongTestCase
import random


def random_range():
    # TODO: make sure this can only be generated once
    return range(random.randint(1000, 2000))


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
