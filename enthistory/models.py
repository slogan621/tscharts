#(C) Copyright Syd Logan 2019-2020
#(C) Copyright Thousand Smiles Foundation 2019-2020
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from __future__ import unicode_literals

from django.db import models

from patient.models import Patient
from clinic.models import Clinic

class ENTHistory(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name

    time = models.DateTimeField(auto_now=True)

    EAR_DURATION_DAYS = 'd'
    EAR_DURATION_WEEKS = 'w'
    EAR_DURATION_MONTHS = 'm'
    EAR_DURATION_INTERMITTENT = 'i'
    EAR_DURATION_PERMANENT = 'p'
    EAR_DURATION_NONE = 'n'

    EAR_DURATION_CHOICES = ((EAR_DURATION_NONE, "none"), (EAR_DURATION_DAYS, "days"), (EAR_DURATION_WEEKS, "weeks"), (EAR_DURATION_MONTHS, "months"), (EAR_DURATION_INTERMITTENT, "intermittent"), (EAR_DURATION_PERMANENT, "permanent"))

    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_NONE = 'n'

    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"), (EAR_SIDE_NONE, "none"))

    drainageSide = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_BOTH)
    drainageDuration = models.CharField(max_length = 1, choices = EAR_DURATION_CHOICES, default = EAR_DURATION_NONE)
    hearingLossSide = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_BOTH)
    hearingLossDuration = models.CharField(max_length = 1, choices = EAR_DURATION_CHOICES, default = EAR_DURATION_NONE)
    painSide = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_BOTH)
    painDuration = models.CharField(max_length = 1, choices = EAR_DURATION_CHOICES, default = EAR_DURATION_NONE)

    comment = models.TextField(default = "")
