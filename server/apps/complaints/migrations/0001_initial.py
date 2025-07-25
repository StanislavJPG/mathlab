# Generated by Django 5.1.11 on 2025-07-09 21:57

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_lifecycle.mixins
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                (
                    'complaint_text',
                    models.TextField(
                        validators=[django.core.validators.MinLengthValidator(35)], verbose_name='complaint text'
                    ),
                ),
                ('processed', models.BooleanField(default=False, verbose_name='processed')),
                (
                    'category',
                    models.CharField(
                        choices=[
                            ('inappropriate', 'Inappropriate content'),
                            ('spam', 'Spam or advertisement'),
                            ('fraud', 'Fraud'),
                            ('offensive', 'Offensive or hateful content'),
                            ('copyright', 'Copyright infringement'),
                            ('misleading', 'Misleading information'),
                            ('scam', 'Scam or phishing'),
                            ('violence', 'Violent or threatening content'),
                            ('harassment', 'Harassment or bullying'),
                            ('duplicate', 'Duplicate or reposted content'),
                            ('fake_item', 'Fake or counterfeit item'),
                            ('wrong_category', 'Wrong category'),
                            ('price_manipulation', 'Price manipulation'),
                            ('fake_profile', 'Fake profile'),
                            ('impersonation', 'Impersonation'),
                            ('other', 'Other'),
                        ],
                        verbose_name='category',
                    ),
                ),
                ('counter', models.PositiveSmallIntegerField(default=0, verbose_name='complaint counter')),
                ('object_id', models.PositiveIntegerField()),
                (
                    'content_type',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
                ),
            ],
            options={
                'verbose_name': 'Complaint',
                'verbose_name_plural': 'Complaints',
                'ordering': ('-created_at', '-counter'),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
