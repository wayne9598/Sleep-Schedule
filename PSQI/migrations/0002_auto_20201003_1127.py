# Generated by Django 3.1.2 on 2020-10-03 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PSQI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psqi',
            name='badDreams',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='coughSnore',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='date',
            field=models.DateField(default=datetime.date(2020, 10, 2)),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='enthusiasmToDoThings',
            field=models.CharField(choices=[('0', 'noProblem'), ('1', 'slightProblem'), ('2', 'someWhatAProblem'), ('3', 'bigProblem')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='feelCold',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='feelHot',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='latencyGreaterThan30',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='midnightAwakeEarlyMorning',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='otherReason',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='pain',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='selfRatedSleepQuality',
            field=models.CharField(choices=[('0', 'VeryGood'), ('1', 'FairlyGood'), ('2', 'FairlyBad'), ('3', 'VeryBad')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='sleepMedication',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='stayAwakeDuringWork',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='uncomfortableBreathing',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='psqi',
            name='useBathroom',
            field=models.CharField(choices=[('0', 'notDuringPastMonth'), ('1', 'lessThanOnceAWeek'), ('2', 'onceTwiceAWeek'), ('3', 'greaterThan3Aweek')], default='1', max_length=20),
        ),
    ]
