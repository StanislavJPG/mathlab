# Generated by Django 5.1.7 on 2025-03-23 22:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('drafts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theoristdrafts',
            name='label',
            field=models.CharField(blank=True, max_length=95, null=True),
        ),
    ]
