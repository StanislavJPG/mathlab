# Generated by Django 5.1.6 on 2025-03-02 15:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0017_comment_supports_post_supports_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_views',
        ),
    ]
