from django.test import TestCase as DjangoTestCase
from django.utils import unittest
import fudge
import random
from contextlib import contextmanager

class SettingDoesNotExist:
    pass

@contextmanager
def patch_settings(**kwargs):
    from django.conf import settings
    old_settings = []
    for key, new_value in kwargs.items():
        old_value = getattr(settings, key, SettingDoesNotExist)
        old_settings.append((key, old_value))
        setattr(settings, key, new_value)
    yield
    for key, old_value in old_settings:
        if old_value is SettingDoesNotExist:
            delattr(settings, key)
        else:
            setattr(settings, key, old_value)


class HatbandTestCase(DjangoTestCase):
    
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()
        

class HatbandTestMixin(object):
    
    def assertCkEditorPresent(self, response):
        self.assertContains(response, '<script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>')
        self.assertContains(response, 'class="ckeditor"></textarea>')
    
    def assertCkEditorNotPresent(self, response):
        self.assertNotContains(response, '<script type="text/javascript" src="/static/ckeditor/ckeditor.js"></script>')
        self.assertNotContains(response, 'class="ckeditor"></textarea>')
        