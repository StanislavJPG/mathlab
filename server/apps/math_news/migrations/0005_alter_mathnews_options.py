# Generated by Django 5.1.7 on 2025-03-16 21:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('math_news', '0004_alter_mathnews_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mathnews',
            options={'get_latest_by': 'created_at', 'ordering': ('created_at',), 'verbose_name_plural': 'news'},
        ),
    ]
