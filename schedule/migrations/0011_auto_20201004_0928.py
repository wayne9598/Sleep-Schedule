# Generated by Django 3.1.2 on 2020-10-04 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_auto_20201004_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleep_schedule',
            name='PSQI_score',
            field=models.IntegerField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sleep_schedule',
            name='sensed_score',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
