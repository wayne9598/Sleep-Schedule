# Generated by Django 3.1.2 on 2020-10-04 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
        ('schedule', '0002_auto_20201004_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleep_schedule',
            name='do_excercise',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='exercise',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise'),
        ),
    ]
