# Generated by Django 3.1.2 on 2020-10-03 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20201003_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleep_schedule',
            name='breakfast_end_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='breakfast_start_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='dinner_end_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='dinner_start_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='excercise_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='excercise_type',
            field=models.CharField(blank=True, choices=[('Aerobics', 'Aerobics'), ('Resistant Training', 'Resistant Training')], default='1', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='exercise_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='lunch_end_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='lunch_start_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AlterField(
            model_name='sleep_schedule',
            name='nap_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sleep_schedule',
            name='nap_start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
