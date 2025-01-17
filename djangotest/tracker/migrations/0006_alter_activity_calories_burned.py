# Generated by Django 5.1.4 on 2025-01-14 22:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_activity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='calories_burned',
            field=models.IntegerField(blank=True, db_index=True, null=True, validators=[django.core.validators.MinValueValidator(0, message='Calories burned cannot be negative'), django.core.validators.MaxValueValidator(5000, message='Calories burned seems too high')]),
        ),
    ]
