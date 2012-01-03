import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.client import Client

from ._utils import HatbandTestCase as TestCase
from .hatband_support.models import *
from .. import autodiscover

autodiscover()

PASSWORD = "password"

__all__ = [
    "GenericKeyFacetsViewTestCase",
    "TypeAndModelToQueryViewTestCase",
    "RenderModelPreviewTestCase",
    "ModelSearchBackfillMixinTestCase",
]


def staff_login(func):
    def inner(self, *args, **kwargs):
        self.client.login(username=self.staff.username, password=PASSWORD)
        return func(self, *args, **kwargs)
    return inner


def admin_login(func):
    def inner(self, *args, **kwargs):
        self.client.login(username=self.admin.username, password=PASSWORD)
        return func(self, *args, **kwargs)
    return inner


class HatbandViewTestCase(TestCase):
    def setUp(self):
        super(HatbandViewTestCase, self).setUp()
        if self.view_name:
            self.url = reverse(self.view_name)
        self.client = Client()
        self.admin = User.objects.create_superuser(
                username="test_admin",
                email="test@example.com",
                password=PASSWORD)
        self.admin.is_superuser = True
        self.admin.save()

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


class ModelSearchBackfillMixinTestCase(HatbandViewTestCase):
    view_name_template = "admin:%s_%s_search"
    view_name = False

    def get_response(self):
        return self.client.get(self.url, {"q": self.content_type.model})

    def setUp(self):
        super(ModelSearchBackfillMixinTestCase, self).setUp()
        self.content_type = ContentType.objects.get(app_label="auth",
                model="user")
        view_name = self.view_name_template % (
                self.content_type.app_label,
                self.content_type.model)
        self.url = reverse(view_name)

    @admin_login
    def test_search_returns_json(self):
        response = self.get_response()
        data = json.loads(response.content)
        self.assertEqual(1, len(data["results"]))
        expected = "%s: %s" % (self.regular_user.pk,
                self.regular_user.username)
        self.assertEqual(expected, data["results"][0])


class TypeAndModelToQueryViewTestCase(HatbandViewTestCase):
    view_name = "admin:type_and_model_to_query"

    def get_response(self):
        content_type = ContentType.objects.get_for_model(User)
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
        content_type = ContentType.objects.get_for_model(User)
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
