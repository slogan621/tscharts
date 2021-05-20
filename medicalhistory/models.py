#(C) Copyright Syd Logan 2017-2021
#(C) Copyright Thousand Smiles Foundation 2017-2021
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

class MedicalHistory(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    time = models.DateTimeField(auto_now=True)
    cold_cough_fever = models.BooleanField(default = False)
    hivaids = models.BooleanField(default = False)
    anemia = models.BooleanField(default = False)
    athsma = models.BooleanField(default = False)
    cancer = models.BooleanField(default = False)
    congenitalheartdefect = models.BooleanField(default = False)
    congenitalheartdefect_workup = models.BooleanField(default = False)
    congenitalheartdefect_planforcare = models.BooleanField(default = False)
    diabetes = models.BooleanField(default = False)
    epilepsy = models.BooleanField(default = False)
    bleeding_problems = models.BooleanField(default = False)
    hepititis = models.BooleanField(default = False)
    tuberculosis = models.BooleanField(default = False)
    troublespeaking = models.BooleanField(default = False)
    troublehearing = models.BooleanField(default = False)
    troubleeating = models.BooleanField(default = False)
    pregnancy_duration = models.IntegerField(default = 9)
    pregnancy_smoke = models.BooleanField(default = False)
    birth_complications = models.BooleanField(default = False)
    pregnancy_complications = models.BooleanField(default = False)
    mother_alcohol = models.BooleanField(default = False)
    relative_cleft = models.BooleanField(default = False)
    parents_cleft = models.BooleanField(default = False)
    siblings_cleft = models.BooleanField(default = False)
    meds = models.TextField()  
    allergymeds = models.TextField()
    first_crawl = models.IntegerField(default=7) 
    first_sit = models.IntegerField(default=8)
    first_words = models.IntegerField(default=12)
    first_walk = models.IntegerField(default=12)
    birth_weight = models.IntegerField(default=0)
    birth_weight_metric = models.BooleanField(default=True)
    height = models.IntegerField(default=0)
    height_metric = models.BooleanField(default=True)
    weight = models.IntegerField(default=0)
    weight_metric = models.BooleanField(default=True)
    born_with_cleft_lip = models.BooleanField(default=False)
    born_with_cleft_palate = models.BooleanField(default=False)
