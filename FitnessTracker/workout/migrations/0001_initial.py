# Generated by Django 4.2 on 2024-04-19 04:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day_number",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Day 1"),
                            (2, "Day 2"),
                            (3, "Day 3"),
                            (4, "Day 4"),
                            (5, "Day 5"),
                            (6, "Day 6"),
                            (7, "Day 7"),
                        ]
                    ),
                ),
            ],
            options={
                "ordering": ["day_number"],
            },
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "five_rep_max",
                    models.FloatField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(1500),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                (
                    "default_weight",
                    models.FloatField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(1500),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                (
                    "default_reps",
                    models.PositiveIntegerField(
                        default=8,
                        validators=[
                            django.core.validators.MaxValueValidator(100),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                (
                    "default_modifier",
                    models.CharField(
                        choices=[
                            ("add", "Add"),
                            ("subtract", "Subtract"),
                            ("percentage", "Percentage"),
                            ("exact", "Exact"),
                        ],
                        default="percentage",
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "name")},
            },
        ),
        migrations.CreateModel(
            name="Routine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "name")},
            },
        ),
        migrations.CreateModel(
            name="WorkoutSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("auto_update_five_rep_max", models.BooleanField(default=False)),
                ("show_rest_timer", models.BooleanField(default=False)),
                ("show_workout_timer", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Workout Settings",
            },
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("config", models.JSONField(default=dict)),
                (
                    "exercises",
                    models.ManyToManyField(blank=True, to="workout.exercise"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "name")},
            },
        ),
        migrations.CreateModel(
            name="Week",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week_number", models.PositiveSmallIntegerField()),
                (
                    "routine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weeks",
                        to="workout.routine",
                    ),
                ),
            ],
            options={
                "ordering": ["week_number"],
                "unique_together": {("routine", "week_number")},
            },
        ),
        migrations.CreateModel(
            name="RoutineSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week_number", models.PositiveSmallIntegerField(default=1)),
                ("day_number", models.PositiveSmallIntegerField(default=1)),
                ("workout_index", models.PositiveSmallIntegerField(default=0)),
                (
                    "last_completed",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "routine",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workout.routine",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Routine Settings",
            },
        ),
        migrations.CreateModel(
            name="DayWorkout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.IntegerField(default=0)),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workout.day"
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workout.workout",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="day",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="days",
                to="workout.week",
            ),
        ),
        migrations.AddField(
            model_name="day",
            name="workouts",
            field=models.ManyToManyField(
                related_name="days", through="workout.DayWorkout", to="workout.workout"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="day",
            unique_together={("week", "day_number")},
        ),
    ]
