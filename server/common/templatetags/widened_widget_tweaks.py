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


@register.simple_tag(takes_context=True)
def render_nonfield_errors(context, small=False, autohide=True, **kwargs):
    """
    HTML example: `{% render_nonfield_errors class="text-warning" %}`
    small attrs verify whether we use <small> tag for errors or not
    """
    form = context.get('form', None)
    if form:
        cls = kwargs.get('class', 'alert alert-danger')
        hs_autohide = '_="on load wait 10s then transition my opacity to 0 then remove me"' if autohide else ''
        text_to_render = (
            f"""
                <div class="{cls}" {hs_autohide}>
                  {'<br>'.join([f'<small>{error}</small>' if small else error for error in form.non_field_errors()])}
                </div>
            """
            if form.non_field_errors()
            else ''
        )
        return format_html(text_to_render)


@register.simple_tag(name='render_form_spinner_attrs')
def render_form_attrs_with_spinner(
    target_spinner_id='wait-spinner',
    with_request_toast=True,  # add 'Wait while loading...' toast while request is processing
):
    toast_trigger = 'data-toast-trigger' if with_request_toast else ''
    attrs_to_render = f'_="on submit toggle @hidden on #{target_spinner_id} until htmx:afterOnLoad" {toast_trigger}'
    return format_html(attrs_to_render)


@register.simple_tag(name='render_submit_button')
def render_bootstrap_spinner_submit_button(
    label='',
    *,
    # `id` and `class` attributes for the spinner to be inside button
    spinner_id='wait-spinner',
    spinner_class='spinner-grow text-light spinner-grow-sm',
    ###
    with_icon=None,  # add <i></i> icon to the button
    **kwargs,
):
    """
    It's recommended to use it with `render_form_spinner_attrs` tag to add spinner while request is processing
    Example:
        ```
        <form hx-post="{{ request.path }}" {% render_form_spinner_attrs %}>
            {% render_field form.username|add_bootstrap_validation_classes class="form-control" %}
            {% render_field_errors form.username %}

            {% translate 'Apply changes' as btn_label %}
            {% render_submit_button btn_label %}
        </form>
        ```
    """
    attrs = ' '.join([f'{k}="{v}"' for k, v in kwargs.items()])
    spinner = f'<div id="{spinner_id}" class="{spinner_class}" role="status" hidden></div>'
    icon = f'<i class="{with_icon}"></i>' if with_icon else ''
    class_ = kwargs.get('class', 'btn btn-primary')

    btn_to_render = f'<button type="submit" class="{class_}" {attrs}>{spinner} {icon} {label}</button>'
    return format_html(btn_to_render)
