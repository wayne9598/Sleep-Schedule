# Generated by Django 3.1.2 on 2020-10-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0007_auto_20201003_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='resting_heart_rate',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]
