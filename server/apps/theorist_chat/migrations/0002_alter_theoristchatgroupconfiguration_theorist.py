# Generated by Django 5.2 on 2025-04-05 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('theorist', '0008_alter_theorist_modified_at_and_more'),
        ('theorist_chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theoristchatgroupconfiguration',
            name='theorist',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name='chat_configuration', to='theorist.theorist'
            ),
        ),
    ]
