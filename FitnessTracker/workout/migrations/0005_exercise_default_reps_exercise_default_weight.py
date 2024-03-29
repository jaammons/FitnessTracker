# Generated by Django 4.2 on 2024-03-01 04:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workout", "0004_workout_exercises"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="default_reps",
            field=models.PositiveIntegerField(
                default=8,
                validators=[
                    django.core.validators.MaxValueValidator(100),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="default_weight",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=6,
                validators=[
                    django.core.validators.MaxValueValidator(1500),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
    ]
