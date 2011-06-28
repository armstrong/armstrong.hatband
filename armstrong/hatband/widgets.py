from django import forms


class HatbandRichTextWidget(forms.Textarea):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'hatbandTextArea'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(HatbandRichTextWidget, self).__init__(attrs=final_attrs)