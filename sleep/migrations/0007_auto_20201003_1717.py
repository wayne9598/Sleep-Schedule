# Generated by Django 3.1.2 on 2020-10-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0006_auto_20201003_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='resting_heart_rate',
            field=models.IntegerField(),
        ),
    ]
