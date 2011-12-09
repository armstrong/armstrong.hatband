import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.client import Client

from ._utils import HatbandTestCase as TestCase
from .hatband_support.models import *

PASSWORD = "password"

__all__ = [
    "GenericKeyFacetsViewTestCase",
    "TypeAndModelToQueryViewTestCase",
    "RenderModelPreviewTestCase",
]


def staff_login(func):
    def inner(self, *args, **kwargs):
        self.client.login(username=self.staff.username, password=PASSWORD)
        return func(self, *args, **kwargs)
    return inner


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

    @staff_login
    def test_query_is_inside_response(self):
        response = self.get_response()
        data = json.loads(response.content)
        self.assertTrue("query" in data)

    @staff_login
    def test_bad_response_on_unknown_content_type(self):
        response = self.client.get(self.url, {"content_type_id": -1})
        self.assertEqual(400, response.status_code)

    @staff_login
    def test_bad_response_on_no_object_id(self):
        content_type = ContentType.objects.all()[0]
        response = self.client.get(self.url,
                {"content_type_id": content_type.pk})
        self.assertEqual(400, response.status_code)

    @staff_login
    def test_returns_empty_query_on_unknown_object_id(self):
        content_type = ContentType.objects.all()[0]
        response = self.client.get(self.url,
                {"content_type_id": content_type.pk, "object_id": -1})
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content)
        self.assertTrue("query" in data)
        self.assertEqual("", data["query"])

    @staff_login
    def test_returns_string_suitable_for_display_in_gfk_widget(self):
        content_type = ContentType.objects.all()[0]
        obj = content_type.model_class().objects.all()[0]
        response = self.client.get(self.url, {
                "content_type_id": content_type.pk,
                "object_id": obj.pk})
        data = json.loads(response.content)
        query = data["query"]
        self.assertEqual('%s: "%d: %s"' % (content_type.model, obj.pk, obj, ),
                         query)


class RenderModelPreviewTestCase(HatbandViewTestCase):
    view_name = "admin:render_model_preview"

    def get_response(self):
        cat = TestCategory.objects.create(name="cat")
        TestArticle.objects.create(text="Hooray", category=cat)
        content_type = ContentType.objects.get_for_model(TestArticle)
        obj = content_type.model_class().objects.all()[0]
        return self.client.get(self.url, {
                "content_type": content_type.pk,
                "object_id": obj.pk})

    def test_template_rendered(self):
        self.client.login(username=self.staff.username, password=PASSWORD)
        response = self.get_response()
        self.assertEqual(response.content, 'It worked! Hooray\n')
