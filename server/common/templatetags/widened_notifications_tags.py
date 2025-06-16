from django.db.models import Q
from django.template.defaultfilters import register
from django.urls import reverse
from django.utils.html import format_html

from server.apps.theorist_chat.models import TheoristMessage


# Requires vanilla-js framework - http://vanilla-js.com/
@register.simple_tag
def widened_register_notify_callbacks(
    badge_class='live_notify_badge',  # pylint: disable=too-many-arguments,missing-docstring
    menu_class='live_notify_list',
    menu_el_class='live_notify_el',  # custom menu_el_class for adding class for <li> elements
    refresh_period=15,
    callbacks='',
    api_name='list',
    fetch=5,
    nonce=None,
    mark_as_read=False,
):
    refresh_period = int(refresh_period) * 1000

    if api_name == 'list':
        api_url = reverse('notifications:live_unread_notification_list')
    elif api_name == 'count':
        api_url = reverse('notifications:live_unread_notification_count')
    else:
        return ''
    definitions = """
        notify_badge_class='{badge_class}';
        notify_menu_class='{menu_class}';
        notify_menu_el_class='{menu_el_class}';
        notify_api_url='{api_url}';
        notify_fetch_count='{fetch_count}';
        notify_unread_url='{unread_url}';
        notify_mark_all_unread_url='{mark_all_unread_url}';
        notify_refresh_period={refresh};
        notify_mark_as_read={mark_as_read};
    """.format(
        badge_class=badge_class,
        menu_class=menu_class,
        menu_el_class=menu_el_class,
        refresh=refresh_period,
        api_url=api_url,
        unread_url=reverse('notifications:unread'),
        mark_all_unread_url=reverse('notifications:mark_all_as_read'),
        fetch_count=fetch,
        mark_as_read=str(mark_as_read).lower(),
    )

    # add a nonce value to the script tag if one is provided
    nonce_str = ' nonce="{nonce}"'.format(nonce=nonce) if nonce else ''

    script = '<script type="text/javascript"{nonce}>'.format(nonce=nonce_str) + definitions
    for callback in callbacks.split(','):
        script += 'register_notifier(' + callback + ');'
    script += '</script>'
    return format_html(script)


@register.simple_tag(name='unread_messages_counter', takes_context=True)
def get_unread_message_notifications_count(context, mailbox, as_html=False):
    theorist = context['request'].theorist
    messages_count = TheoristMessage.objects.filter(~Q(sender=theorist), room=mailbox, is_read=False).count()
    html_message_count = (
        format_html(f'<span class="badge bg-danger float-end">{messages_count}</span>') if messages_count > 0 else ''
    )
    return html_message_count if as_html else messages_count
