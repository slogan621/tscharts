#(C) Copyright Syd Logan 2020
#(C) Copyright Thousand Smiles Foundation 2020
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
from dentalcdt.models import DentalCDT

class DentalState(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name
    time = models.DateTimeField(auto_now=True)
    tooth = models.IntegerField(default = 9999)
    code = models.ForeignKey(DentalCDT)

    DENTAL_STATE_NONE = 'n'
    DENTAL_STATE_UNTREATED = 'u'
    DENTAL_STATE_TREATED = 't'
    DENTAL_STATE_OTHER = 'o'

    DENTAL_STATE_CHOICES = ((DENTAL_STATE_NONE, "none"), (DENTAL_STATE_UNTREATED, "untreated"), (DENTAL_STATE_TREATED, "treated"), (DENTAL_STATE_OTHER, "other"))

    state = models.CharField(max_length = 1, choices = DENTAL_STATE_CHOICES, default = DENTAL_STATE_NONE)

    comment = models.TextField(default = "")
