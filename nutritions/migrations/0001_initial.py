# Generated by Django 3.1.2 on 2020-10-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_protein', models.FloatField()),
                ('m_fat_saturated', models.FloatField()),
                ('m_fat_unsaturated', models.FloatField()),
                ('m_carb', models.FloatField()),
                ('m_sugar', models.FloatField()),
                ('m_NaCl', models.FloatField()),
                ('m_potassium', models.FloatField()),
            ],
        ),
    ]
