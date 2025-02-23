from django.template.defaultfilters import register
from django.utils.html import format_html
from widget_tweaks.templatetags.widget_tweaks import add_class


@register.filter('add_bootstrap_validation_classes')
def add_bootstrap_validation_classes(field):
    if field.form.is_bound:
        if field.errors:
            css_class = 'is-invalid'
        else:
            css_class = 'is-valid'
        return add_class(field, css_class)
    return field


@register.simple_tag
def render_field_errors(field, class_='text-danger mb-2', sophisticated=False):
    """
    HTML example: `{% render_field_errors form.email class_="invalid-feedback" %}`
    sophisticated attrs verify whether we use <small> tag for errors or not
    """
    text_to_render = f"""
        <div class="{class_}">
          {'<br>'.join([f'<small>{error}</small>' if sophisticated else error for error in field.errors])}
        </div>
    """
    return format_html(text_to_render)
