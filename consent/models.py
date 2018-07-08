# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from register.models import Register
from patient.models import Patient
from clinic.models import Clinic

class Consent(models.Model):
    registration = models.ForeignKey(Register)
    patient = models.ForeignKey(Patient)
    clinic = models.ForeignKey(Clinic)
    general_consent = models.BooleanField(default = False)
    photo_consent = models.BooleanField(default = False)
