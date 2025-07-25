# Generated by Django 5.1.11 on 2025-07-13 20:40

import django_bleach.models
import dynamic_filenames
from django.db import migrations, models
import server.common.validators


class Migration(migrations.Migration):
    dependencies = [
        ('theorist_chat', '0006_theoristmessage_is_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='theoristmessage',
            name='audio_message',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern='{app_label:.25}/rooms/{instance.room.uuid}/{instance.sender.full_name_slug}/audio/{uuid:s}{ext}'
                ),
                validators=[server.common.validators.validate_audio_ext],
            ),
        ),
        migrations.AlterField(
            model_name='theoristmessage',
            name='message',
            field=django_bleach.models.BleachField(blank=True, max_length=500),
        ),
    ]
