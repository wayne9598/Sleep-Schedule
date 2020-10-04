# Generated by Django 3.1.2 on 2020-10-04 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20201004_0840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sleep_schedule',
            old_name='caffeine',
            new_name='take_caffeine',
        ),
        migrations.RenameField(
            model_name='sleep_schedule',
            old_name='melatonin',
            new_name='take_meditation',
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='take_melatonin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
