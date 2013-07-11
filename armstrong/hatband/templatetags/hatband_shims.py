from django import VERSION
from django.template import Library, Node

register = Library()


class AdminMediaPrefixShimNode(Node):
    def __init__(self, admin_media_prefix):
        self.admin_media_prefix = admin_media_prefix

    def render(self, context):
        return self.admin_media_prefix


def do_admin_media_prefix(parser, token):
    if VERSION[0] == 1 and VERSION[1] < 4:
        from django.contrib.admin.templatetags.adminmedia import admin_media_prefix
        return AdminMediaPrefixShimNode(admin_media_prefix())
    else:
        from django.contrib.staticfiles.templatetags.staticfiles import do_static
        from django.template.base import Token, TOKEN_TEXT
        return do_static(parser, Token(TOKEN_TEXT, "static 'admin/'"))
register.tag('admin_media_prefix_shim', do_admin_media_prefix)
