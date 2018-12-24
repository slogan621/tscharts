#(C) Copyright Syd Logan 2019
#(C) Copyright Thousand Smiles Foundation 2019
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

# Create your models here.

from clinic.models import Clinic
from patient.models import Patient
from clinicstation.models import ClinicStation

class ReturnToClinicStation(models.Model):

    SCHEDULED = 's'
    CREATED = 'c'
    STATE_CHOICES = ((SCHEDULED, "scheduled"), (CREATED, "created"))

    state = models.CharField(
        max_length = 1,
        choices = STATE_CHOICES,
        default = CREATED,
    )
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    clinicstation = models.ForeignKey(ClinicStation, related_name="clinicstations")
    requestingclinicstation = models.ForeignKey(ClinicStation, related_name="requestingclinicstations")
    createtime = models.DateTimeField(auto_now_add=True)
    statechangetime = models.DateTimeField(auto_now=True)
