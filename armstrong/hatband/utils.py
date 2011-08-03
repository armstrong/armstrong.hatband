from django.conf import settings


# TODO: move this over to somewhere more appropriate
def static_url(url):
    return ''.join((settings.STATIC_URL, url))
