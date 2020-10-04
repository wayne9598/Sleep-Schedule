from django.db import models

# Create your models here.

class Astronaut(models.Model):

    GENDER_CHOICES = ( 
        ("MALE", "MALE"), 
        ("FEMALE", "FEMALE"), 
    )

    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES)

    def __str__(self):
        return '%s' % (self.name)