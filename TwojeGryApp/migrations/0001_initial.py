# Generated by Django 5.0.1 on 2024-01-22 15:30

import TwojeGryApp.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone_number', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('genre', models.IntegerField(choices=[(TwojeGryApp.models.Genre['Euro'], 1), (TwojeGryApp.models.Genre['Ameritrash'], 2), (TwojeGryApp.models.Genre['ForKids'], 3), (TwojeGryApp.models.Genre['Family'], 4), (TwojeGryApp.models.Genre['Party'], 5), (TwojeGryApp.models.Genre['Economical'], 6), (TwojeGryApp.models.Genre['Strategic'], 7), (TwojeGryApp.models.Genre['Cooperative'], 8), (TwojeGryApp.models.Genre['War'], 9), (TwojeGryApp.models.Genre['Battle'], 10), (TwojeGryApp.models.Genre['Hybrid'], 11), (TwojeGryApp.models.Genre['Card'], 12)])),
                ('min_players', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_per_delayed_day', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='GameCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_bought', models.DateTimeField()),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TwojeGryApp.game')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_ordered', models.DateTimeField()),
                ('time_returned', models.DateTimeField(blank=True, null=True)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TwojeGryApp.client')),
                ('game_copy_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TwojeGryApp.gamecopy')),
            ],
        ),
    ]