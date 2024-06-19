# Generated by Django 4.2.7 on 2024-06-18 21:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MathNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('new_url', models.CharField(max_length=255, unique=True)),
                ('additional_info', models.CharField(max_length=255, null=True)),
                ('posted', models.CharField(max_length=100)),
                ('published_at', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'news',
                'ordering': ('title',),
                'get_latest_by': 'published_at',
            },
        ),
    ]
