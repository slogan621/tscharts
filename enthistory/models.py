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

from patient.models import Patient
from clinic.models import Clinic

class ENTHistory(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name

    time = models.DateTimeField(auto_now=True)

    ENT_TYPE_HEARING_LOSS = 'm'
    ENT_TYPE_DRAINAGE = 'd'
    ENT_TYPE_PAIN = 'p'
    ENT_TYPE_OTHER = 'o'
    ENT_TYPE_CHOICES = ((ENT_TYPE_HEARING_LOSS, "hearing loss"), (ENT_TYPE_DRAINAGE, "drainage"), (ENT_TYPE_PAIN, "pain"), (ENT_TYPE_OTHER, "other"))
    type = models.CharField(max_length = 1, choices = ENT_TYPE_CHOICES, default = ENT_TYPE_OTHER)

    '''
    If type == ENT_TYPE_OTHER, name supplies the name of the condition.
    Otherwise, name is ignored.
    '''

    name = models.CharField(max_length = 32, default = "")

    EAR_DURATION_NONE = 'n'
    EAR_DURATION_DAYS = 'd'
    EAR_DURATION_WEEKS = 'w'
    EAR_DURATION_MONTHS = 'm'
    EAR_DURATION_INTERMITTENT = 'i'

    EAR_DURATION_CHOICES = ((EAR_DURATION_NONE, "none"), (EAR_DURATION_DAYS, "days"), (EAR_DURATION_WEEKS, "weeks"), (EAR_DURATION_MONTHS, "months"), (EAR_DURATION_INTERMITTENT, "intermittent"))
    duration = models.CharField(max_length = 1, choices = EAR_DURATION_CHOICES, default = EAR_DURATION_NONE)

    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"))

    side = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_BOTH)
    comment = models.TextField(default = "")
