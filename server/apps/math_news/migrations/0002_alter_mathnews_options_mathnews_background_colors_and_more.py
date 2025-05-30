# Generated by Django 5.1.7 on 2025-03-15 21:58

import django.contrib.postgres.fields
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('math_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mathnews',
            options={'get_latest_by': 'published_at', 'ordering': ('published_at',), 'verbose_name_plural': 'news'},
        ),
        migrations.AddField(
            model_name='mathnews',
            name='background_colors',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=200), blank=True, default=['#eeaeca', '#94bbe9'], size=2
            ),
        ),
        migrations.AddField(
            model_name='mathnews',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='mathnews',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='mathnews',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='mathnews',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
