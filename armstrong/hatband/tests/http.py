import json
import random

from ._utils import HatbandTestCase as TestCase

from ..http import JsonResponse


class JsonResponseTestCase(TestCase):
    def test_turns_body_into_json(self):
        data = {
            "foo": "bar",
            "random": random.randint(1000, 2000),
        }

        response = JsonResponse(data)
        self.assertIsA(response.content, str, msg="sanity check")
        self.assertEqual(json.loads(response.content), data)
