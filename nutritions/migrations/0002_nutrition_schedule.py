# Generated by Django 3.1.2 on 2020-10-04 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0001_initial'),
        ('nutritions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutrition',
            name='schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.sleep_schedule'),
        ),
    ]
