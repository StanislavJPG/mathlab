from django import forms


class GraphBuilderForm(forms.Form):
    function = forms.CharField(max_length=100, required=True)
