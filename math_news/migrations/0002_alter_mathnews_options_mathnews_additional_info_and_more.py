# Generated by Django 4.2.7 on 2024-05-09 20:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('math_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mathnews',
            options={'get_latest_by': 'published_at', 'ordering': ('title',), 'verbose_name_plural': 'news'},
        ),
        migrations.AddField(
            model_name='mathnews',
            name='additional_info',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mathnews',
            name='published_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='mathnews',
            name='new_url',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='mathnews',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterModelTable(
            name='mathnews',
            table=None,
        ),
    ]
