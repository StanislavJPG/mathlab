from django.template.defaultfilters import register
from widget_tweaks.templatetags.widget_tweaks import add_class


@register.filter("add_bootstrap_validation")
def add_bootstrap_validation(field):
    if field.form.is_bound:
        if field.errors:
            css_class = "is-invalid"
        else:
            css_class = "is-valid"
        return add_class(field, css_class)
    return field
