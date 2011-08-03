from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from django.contrib.admin.widgets import *
from .base import RichTextWidget
from .ckeditor import CKEditorWidget
from .visualsearch import GenericKeyWidget
