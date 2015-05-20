import json
import random

from ._utils import HatbandTestCase

from armstrong.hatband.http import JsonResponse


class JsonResponseTestCase(HatbandTestCase):
    def test_turns_body_into_json(self):
        data = {
            "foo": "bar",
            "random": random.randint(1000, 2000),
        }

        response = JsonResponse(data)
        self.assertIsInstance(response.content, basestring)
        self.assertEqual(json.loads(response.content), data)
