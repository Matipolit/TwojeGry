# Generated by Django 5.0.1 on 2024-01-27 14:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("TwojeGryApp", "0002_alter_game_genre"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="time_ordered",
        ),
        migrations.RemoveField(
            model_name="order",
            name="time_returned",
        ),
        migrations.AddField(
            model_name="order",
            name="date_ordered",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="date_returned",
            field=models.DateField(blank=True, null=True),
        ),
    ]