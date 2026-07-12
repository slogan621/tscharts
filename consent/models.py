# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from register.models import Register
from patient.models import Patient
from clinic.models import Clinic

class Consent(models.Model):
    registration = models.ForeignKey(Register, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    general_consent = models.BooleanField(default = False)
    photo_consent = models.BooleanField(default = False)
