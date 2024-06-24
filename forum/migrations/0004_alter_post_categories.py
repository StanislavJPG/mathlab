# Generated by Django 5.0.6 on 2024-06-24 19:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_remove_post_categories_delete_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('GF', 'Графіки функцій'), ('MT', 'Матриці'), ('RV', 'Рівняння'), ('NR', 'Нерівності'), ('SM', 'Системи'), ('VM', 'Вища математика'), ('TY', 'Теорії ймовірностей'), ('KM', 'Комбінаторика'), ('DM', 'Дискретна математика'), ('PM', 'Початкова математика'), ('VD', 'Відсотки'), ('TG', 'Тригонометрія'), ('GM', 'Геометрія'), ('YS', 'Ймовірність і статистика'), ('AL', 'Алгоритми'), ('AG', 'Алгебра'), ('IN', 'Інше')], default='IN', max_length=20), default=('IN',), size=4),
        ),
    ]
