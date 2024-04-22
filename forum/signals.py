import os

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from forum.models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    html_content = render_to_string('forum/forum_notification.html', context={'instance': instance})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        f'[MathLab] Відповідь на Ваше запитання «{instance.post.title}» від {instance.user.username}!',
        text_content,
        os.getenv('MAIL_NAME'),
        ['samper.stas@gmail.com'],  # change to user's email like instance.post.user.email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
