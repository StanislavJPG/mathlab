# Generated by Django 4.2.7 on 2024-05-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_news', '0003_alter_mathnews_new_url_alter_mathnews_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='mathnews',
            name='additional_info',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
