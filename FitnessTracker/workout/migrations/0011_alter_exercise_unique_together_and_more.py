# Generated by Django 4.2 on 2024-03-17 00:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workout', '0010_exercise_default_modifier'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='exercise',
            unique_together={('user', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='workout',
            unique_together={('user', 'name')},
        ),
    ]
