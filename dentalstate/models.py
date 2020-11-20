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
    DENTAL_STATE_MISSING = 'm'

    DENTAL_STATE_CHOICES = ((DENTAL_STATE_MISSING, "missing"), (DENTAL_STATE_NONE, "none"), (DENTAL_STATE_UNTREATED, "untreated"), (DENTAL_STATE_TREATED, "treated"), (DENTAL_STATE_OTHER, "other"))

    state = models.CharField(max_length = 1, choices = DENTAL_STATE_CHOICES, default = DENTAL_STATE_NONE)

    DENTAL_SURFACE_NONE = 'n'
    DENTAL_SURFACE_BUCCAL = 'b'
    DENTAL_SURFACE_LINGUAL = 'u'
    DENTAL_SURFACE_MESIAL = 'm'
    DENTAL_SURFACE_OCCLUSAL = 'c'
    DENTAL_SURFACE_LABIAL = 'a'
    DENTAL_SURFACE_INCISAL = 'i'
    DENTAL_SURFACE_WHOLE_MOUTH_OR_VISIT = 'w'
    DENTAL_SURFACE_OTHER = 'o'

    DENTAL_SURFACE_CHOICES = ((DENTAL_SURFACE_NONE, "none"), (DENTAL_SURFACE_BUCCAL, "buccal"), (DENTAL_SURFACE_LINGUAL, "lingual"), (DENTAL_SURFACE_MESIAL, "mesial"), (DENTAL_SURFACE_OCCLUSAL, 'occlusal'), (DENTAL_SURFACE_LABIAL, 'labial'), (DENTAL_SURFACE_INCISAL, 'incisal'), (DENTAL_SURFACE_WHOLE_MOUTH_OR_VISIT, 'whole_mouth_or_visit'), (DENTAL_SURFACE_OTHER, 'other'))

    # here we define a charfield as a string to hold a set of surfaces
    # this won't work with forms, but since we are just a REST API, doesn't
    # matter much. The DENTAL_STATE_CHOICES tuple will be useful as we
    # serialize/unserialize values between the client and the model. We
    # could also have done this as an integer bitmask, but a string of chars
    # facilitates debugging.

    surface = models.CharField(max_length = 10, choices = DENTAL_SURFACE_CHOICES, default = DENTAL_SURFACE_NONE)

    comment = models.TextField(default = "")
