# Generated by Django 4.2 on 2024-03-02 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workout", "0005_exercise_default_reps_exercise_default_weight"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workout",
            name="exercises",
            field=models.ManyToManyField(blank=True, to="workout.exercise"),
        ),
    ]
