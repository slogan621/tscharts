#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2017
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

class Register(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    timein = models.DateTimeField(auto_now_add=True)
    timeout = models.DateTimeField(auto_now_add=True)
    IN = 'i'
    OUT = 'o'
    STATE_CHOICES = ((IN, "Checked In"), (OUT, "Checked Out"))
    state = models.CharField(
        max_length = 1,
        choices = STATE_CHOICES,
        default = IN,
    )
