from __future__ import unicode_literals

from django.db import models

from patient.models import Patient
from clinicstation.models import ClinicStation

class StateChange(models.Model):
    clinicstation = models.ForeignKey(ClinicStation)
    patient = models.ForeignKey(Patient)
    time = models.DateTimeField(auto_now_add=True)

    IN = 'i'
    OUT = 'o'
    STATE_CHOICES = ((IN, "In"), (OUT, "Out"),)

    state = models.CharField(
        max_length = 1,
        choices = STATE_CHOICES,
        default = OUT,
    )
