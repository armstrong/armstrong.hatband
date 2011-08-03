from django.http import HttpResponse
import json


def json_response(func):
    def inner(*args, **kwargs):
        data = func(*args, **kwargs)
        return HttpResponse(json.dumps(data))
    return inner
