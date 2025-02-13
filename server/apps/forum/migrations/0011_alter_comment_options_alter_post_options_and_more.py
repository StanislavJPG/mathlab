# Generated by Django 5.0.10 on 2025-02-13 10:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0010_auto_20250212_2349"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "get_latest_by": "created_at",
                "ordering": ("created_at",),
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
            },
        ),
        migrations.AlterModelOptions(
            name="post",
            options={
                "get_latest_by": "created_at",
                "ordering": ("created_at",),
                "verbose_name": "post",
                "verbose_name_plural": "posts",
            },
        ),
        migrations.AlterField(
            model_name="comment",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
