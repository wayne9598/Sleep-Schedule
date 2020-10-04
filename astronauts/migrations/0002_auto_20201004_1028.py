# Generated by Django 3.1.2 on 2020-10-04 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astronauts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astronaut',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='astronaut',
            name='weight',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
