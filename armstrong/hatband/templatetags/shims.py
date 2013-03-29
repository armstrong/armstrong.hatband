from django import VERSION
from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def admin_media_prefix():
    if VERSION[0] == 1 and VERSION[1] < 4:
        from django.contrib.admin.templatetags.adminmedia import admin_media_prefix
        return admin_media_prefix()
    else:
        return settings.STATIC_URL + 'admin/'
