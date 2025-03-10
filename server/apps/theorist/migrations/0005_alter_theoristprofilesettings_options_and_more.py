# Generated by Django 5.1.6 on 2025-03-08 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('theorist', '0004_theoristprofilesettings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theoristprofilesettings',
            options={'verbose_name': 'theorist profile setting', 'verbose_name_plural': 'theorist profile settings'},
        ),
        migrations.AddField(
            model_name='theorist',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='About me'),
        ),
    ]
