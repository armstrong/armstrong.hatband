from .http import JsonResponse


def json_response(func):
    """
    Wrap the return value as a JsonResponse object

    Prefered method is to use JsonResponse directly now.

    .. deprecated:: 1.2
    """
    def inner(*args, **kwargs):
        data = func(*args, **kwargs)
        return JsonResponse(data)
    return inner
