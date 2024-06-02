# Generated by Django 4.2.7 on 2024-06-02 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=150, verbose_name='rank')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.rank'),
        ),
    ]
