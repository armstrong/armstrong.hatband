from django.http import HttpResponse
import json


class JsonResponse(HttpResponse):
    """
    Simple HttpResponse object that takes a JSON value as it's parameter

    TODO: Find a proper home for this.
    """
    def __init__(self, data, *args, **kwargs):
        super(JsonResponse, self).__init__(json.dumps(data), *args, **kwargs)
