import os

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from server.apps.forum.models import Comment


@shared_task
def send_notification(comment_id):
    comment = Comment.objects.select_related("post", "user").get(pk=comment_id)
    html_content = render_to_string(
        "forum/forum_notification.html", context={"instance": comment}
    )
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=f"[MathLab] Відповідь на Ваше запитання «{comment.post.title}» від {comment.user.username}!",
        body=text_content,
        from_email=os.getenv("MAIL_NAME"),
        to=(
            comment.post.user.email,
        ),  # change to user's email like instance.post.user.email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


@receiver(post_save, sender=Comment)
def mail_receiver(sender, instance, **kwargs):
    send_notification.delay(instance.pk)
