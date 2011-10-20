from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.client import Client

from ._utils import HatbandTestCase as TestCase

PASSWORD = "password"

__all__ = [
    "GenericKeyFacetsViewTestCase",
    "TypeAndModelToQueryViewTestCase",
]

class HatbandViewTestCase(TestCase):
    def setUp(self):
        super(HatbandViewTestCase, self).setUp()
        self.url = reverse(self.view_name)
        self.client = Client()
        self.admin = User.objects.create_superuser(
                username="test_admin",
                email="test@example.com",
                password=PASSWORD)

        self.staff = User.objects.create_user(
                username="test_staff",
                email="test_staff@example.com",
                password=PASSWORD)
        self.staff.is_staff = True
        self.staff.save()

        self.regular_user = User.objects.create_user(
                username="joe_user",
                email="joe_user@example.com",
                password=PASSWORD)

    def get_response(self):
        return self.client.get(self.url)

    def assert_not_pattern_for_user(self, user, pattern):
        self.client.login(username=user.username, password=PASSWORD)
        response = self.get_response()
        self.assertNotRegexpMatches(response.content, pattern)
        self.client.logout()

    def assert_not_allowed(self, user=None):
        if user is not None:
            self.client.login(username=user.username, password=PASSWORD)
        response = self.get_response()
        self.assertRegexpMatches(response.content,
                r'<input id="id_username"')
        if user is not None:
            self.client.logout()

    def test_requires_staff_user(self):
        self.assert_not_allowed(user=None)

        pattern = r'<input id="id_username"'
        self.assert_not_pattern_for_user(self.admin, pattern)
        self.assert_not_pattern_for_user(self.staff, pattern)

        self.regular_user.is_staff = True
        self.assert_not_allowed(self.regular_user)


class GenericKeyFacetsViewTestCase(HatbandViewTestCase):
    view_name = "admin:generic_key_facets"


class TypeAndModelToQueryViewTestCase(HatbandViewTestCase):
    view_name = "admin:type_and_model_to_query"

    def get_response(self):
        content_type = ContentType.objects.all()[0]
        obj = content_type.model_class().objects.all()[0]
        return self.client.get(self.url, {
                "content_type_id": content_type.pk,
                "object_id": obj.pk})
