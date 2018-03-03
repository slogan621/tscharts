# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your views here.
from patient.models import Patient
from surgerytype.models import SurgeryType

class SurgeryHistory(models.Model):
    patient = models.ForeignKey(Patient)
    surgery = models.ForeignKey(SurgeryType)
    surgeryyear = models.IntegerField(default = 0)
    surgerymonth = models.IntegerField(default = 0)
    surgerylocation =  models.CharField(max_length = 300)
    anesthesia_problems = models.BooleanField(default = False)
    bleeding_problems = models.BooleanField(default = False)

