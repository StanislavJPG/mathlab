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
def render_field_errors(field, class_='text-danger mb-2', small=False):
    """
    HTML example: `{% render_field_errors form.email class_="invalid-feedback" %}`
    small attrs verify whether we use <small> tag for errors or not
    """
    text_to_render = f"""
        <div class="{class_}">
          {'<br>'.join([f'<small>{error}</small>' if small else error for error in field.errors])}
        </div>
    """
    return format_html(text_to_render)


@register.simple_tag(name='render_form_spinner_attrs')
def render_form_attrs_with_spinner(target_spinner_id='wait-spinner'):
    attrs_to_render = f'_="on submit toggle @hidden on #{target_spinner_id} until htmx:afterOnLoad"'
    return format_html(attrs_to_render)


@register.simple_tag(name='render_submit_button')
def render_bootstrap_spinner_submit_button(
    label='',
    *,
    spinner_id='wait-spinner',
    spinner_class='spinner-grow text-light spinner-grow-sm',
    with_icon=None,
    **kwargs,
):
    attrs = ' '.join([f'{k}="{v}"' for k, v in kwargs.items()])
    spinner = f'<div id="{spinner_id}" class="{spinner_class}" role="status" hidden></div>'
    icon = f'<i class="{with_icon}"></i>' if with_icon else ''
    class_ = kwargs.get('class', 'btn btn-primary')

    btn_to_render = f'<button type="submit" class="{class_}" {attrs}>{spinner} {icon} {label}</button>'
    return format_html(btn_to_render)
