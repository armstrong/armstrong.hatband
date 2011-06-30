from django.test import TestCase as DjangoTestCase
from django.utils import unittest
import fudge
import random


class HatbandTestCase(DjangoTestCase):
    
    def setUp(self):
        fudge.clear_expectations()
        fudge.clear_calls()