#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2016
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

from clinic.models import Clinic
from station.models import Station
from patient.models import Patient

class Image(models.Model):
    clinic = models.ForeignKey(Clinic, null=True)
    station = models.ForeignKey(Station, null=True)
    patient = models.ForeignKey(Patient)
    XRAY = 'x'
    HEADSHOT = 'h'
    SURGERY = 's'
    IMAGETYPE_CHOICES = ((XRAY, "Xray"), (HEADSHOT, "Headshot"),
                         (SURGERY, "Surgery"))
    imagetype = models.CharField(
        max_length = 1,
        choices = IMAGETYPE_CHOICES
    )
    path = models.TextField(default = "")
    timestamp = models.DateField(auto_now=True)
