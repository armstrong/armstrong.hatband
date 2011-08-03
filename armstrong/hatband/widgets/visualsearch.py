from django.forms import Widget
from django.template.loader import render_to_string

from ..utils import static_url


class GenericKeyWidget(Widget):
    template = "admin/hatband/widgets/generickey.html"

    class Media:
        js = (static_url("visualsearch/dependencies.js"),
              static_url("visualsearch/visualsearch.js"),
              static_url("generickey.js"),
             )

        css = {
            "all": (static_url("visualsearch/visualsearch.css"),
                    static_url("hatband/css/generickey.css"),
                   )
        }


    def __init__(self, *args, **kwargs):
        super(GenericKeyWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs["value"] = value
        final_attrs["is_templated"] = final_attrs["id"].find("__prefix__") > -1
        return render_to_string(self.template, final_attrs)
