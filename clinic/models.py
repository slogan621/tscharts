from __future__ import unicode_literals

from django.db import models

# Create your models here.

#  {location:location, start:date, end:date}

class Clinic(models.Model):
    location = models.CharField(max_length=30)
    start = models.DateField()
    end = models.DateField()
