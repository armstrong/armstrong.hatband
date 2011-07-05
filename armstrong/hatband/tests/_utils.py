from armstrong.dev.tests.utils import ArmstrongTestCase
from django.utils import unittest
import fudge
import random

class HatbandTestCase(ArmstrongTestCase):
    pass

class HatbandTestMixin(object):
    
    def assertCkEditorPresent(self, response):
        self.assertContains(response, '<script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>')
        self.assertContains(response, 'class="ckeditor"></textarea>')
    
    def assertCkEditorNotPresent(self, response):
        self.assertNotContains(response, '<script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>')
        self.assertNotContains(response, 'class="ckeditor"></textarea>')
        