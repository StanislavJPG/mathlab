# Generated by Django 5.0.10 on 2025-02-12 21:48
import uuid
from django.db import migrations


def gen_uuid(apps, schema_editor):
    # to figure out what's going on here check url below:
    # https://docs.djangoproject.com/en/5.0/howto/writing-migrations/#migrations-that-add-unique-fields
    Comment = apps.get_model("forum", "Comment")
    Post = apps.get_model("forum", "Post")

    for row in Comment.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])

    for row in Post.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0008_alter_comment_options_comment_uuid_post_uuid_and_more"),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
