# Generated by Django 5.0.2 on 2024-03-24 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("workout", "0014_alter_cardiolog_distance"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cardiolog",
            old_name="date",
            new_name="datetime",
        ),
    ]
