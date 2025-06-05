from django import forms

from server.common.third_party_apps.tinymce import DEFAULT_JS_MEDIA_FILES


class TinyMCEMediaFormMixin(forms.Form):
    @property
    def media(self):
        return forms.Media(js=DEFAULT_JS_MEDIA_FILES)
