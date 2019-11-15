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

class ENTSurgicalHistory(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name
    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_NONE = 'n'
    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"), (EAR_SIDE_NONE, "none"))

    tubes = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tubescomment = models.TextField(default = "")
    tplasty = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tplastycomment = models.TextField(default = "")
    eua = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    euacomment = models.TextField(default = "")
    fb = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    fbcomment = models.TextField(default = "")
    myringotomy = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    myringotomycomment = models.TextField(default = "")
    cerumen = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    cerumencomment = models.TextField(default = "")
    granuloma = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    granulomacomment = models.TextField(default = "")
    septorhinoplasty = models.BooleanField(default = False)
    septorhinoplastycomment = models.TextField(default = "")
    scarrevision = models.BooleanField(default = False)
    scarrevisioncomment = models.TextField(default = "")
    frenulectomy = models.BooleanField(default = False)
    frenulectomycomment = models.TextField(default = "")
    time = models.DateTimeField(auto_now=True)
