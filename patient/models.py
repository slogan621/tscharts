from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Patient(models.Model):
    paternal_last = models.CharField(max_length=30)
    maternal_last = models.CharField(max_length=30)
    first = models.CharField(max_length=30)
    middle = models.CharField(max_length=30)
    suffix = models.CharField(max_length=30)
    prefix = models.CharField(max_length=30)
    dob = models.DateField()
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    gender = models.CharField(
        max_length = 1,
        choices = GENDER_CHOICES,
        default = FEMALE,
    )
