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

class ENTTreatment(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name

    time = models.DateTimeField(auto_now=True)

    # if True, treatment is for a future clinic

    future = models.BooleanField(default = False)

    ENT_TREATMENT_CLEANED = 'a'
    ENT_TREATMENT_AUDIOGRAM = 'b'
    ENT_TREATMENT_TYMPANOGRAM = 'c'
    ENT_TREATMENT_MASTOID_DEBRIDED = 'd'
    ENT_TREATMENT_HEARING_AID_EVAL = 'e'
    ENT_TREATMENT_ANTIBIOTIC_DROPS = 'f'
    ENT_TREATMENT_ANTIBIOTIC_ORALLY = 'g'
    ENT_TREATMENT_ANTIBIOTIC_FOR_ACUTE_INFECTION = 'h'
    ENT_TREATMENT_ANTIBIOTIC_FOR_AFTER_WATER_INFECTION_PROTECTION = 'i'
    ENT_TREATMENT_BORIC_ACID_TODAY = 'j'
    ENT_TREATMENT_BORIC_ACID_AT_HOME = 'k'
    ENT_TREATMENT_TUBE_REMOVED = 'l'
    ENT_TREATMENT_FOREIGN_BODY_REMOVED = 'm'
    ENT_TREATMENT_REFERRED_PVT_ENSENADA = 'n'
    ENT_TREATMENT_REFERRED_CHILDRENS_HOSP_TIJUANA = 'o'
    ENT_TREATMENT_SURGERY_TUBES = 'p'
    ENT_TREATMENT_SURGERY_TPLASTY = 'q'
    ENT_TREATMENT_SURGERY_EUA = 'r'
    ENT_TREATMENT_SURGERY_FB = 's'
    ENT_TREATMENT_SURGERY_MIDDLE_EAR_MYRINGOTOMY = 't'
    ENT_TREATMENT_SURGERY_CERUMEN_REMOVAL = 'u'
    ENT_TREATMENT_SURGERY_GRANULOMA_REMOVAL = 'v'
    ENT_TREATMENT_SURGERY_SEPTORHINOPLASTY = 'w'
    ENT_TREATMENT_SURGERY_SCAR_REVISION_CLEFT_LIP = 'x'
    ENT_TREATMENT_SURGERY_FRENULECTOMY = 'y'
    ENT_TREATMENT_OTHER = 'z'

    ENT_TREATMENT_CHOICES = (
        (ENT_TREATMENT_CLEANED, "cleaned"),
        (ENT_TREATMENT_AUDIOGRAM, "audiogram"),
        (ENT_TREATMENT_TYMPANOGRAM, "tympanogram"),
        (ENT_TREATMENT_MASTOID_DEBRIDED, "mastoid debrided"),
        (ENT_TREATMENT_HEARING_AID_EVAL, "hearing aid eval"),
        (ENT_TREATMENT_ANTIBIOTIC_DROPS, "antibiotic drops"),
        (ENT_TREATMENT_ANTIBIOTIC_ORALLY, "antibiotic orally"),
        (ENT_TREATMENT_ANTIBIOTIC_FOR_ACUTE_INFECTION, "antibiotic acute"),
        (ENT_TREATMENT_ANTIBIOTIC_FOR_AFTER_WATER_INFECTION_PROTECTION, "antibiotic water"),
        (ENT_TREATMENT_BORIC_ACID_TODAY, "boric acid today"),
        (ENT_TREATMENT_BORIC_ACID_AT_HOME, "boric acid home"),
        (ENT_TREATMENT_TUBE_REMOVED, "tube removed"),
        (ENT_TREATMENT_FOREIGN_BODY_REMOVED, "foreign body removed"),
        (ENT_TREATMENT_REFERRED_PVT_ENSENADA, "referred ensenada"),
        (ENT_TREATMENT_REFERRED_CHILDRENS_HOSP_TIJUANA, "referred childrens tijuana"),
        (ENT_TREATMENT_SURGERY_TUBES, "surgery tubes"),
        (ENT_TREATMENT_SURGERY_TPLASTY, "surgery tplasty"),
        (ENT_TREATMENT_SURGERY_EUA, "surgery eua"),
        (ENT_TREATMENT_SURGERY_FB, "surgery fb"),
        (ENT_TREATMENT_SURGERY_MIDDLE_EAR_MYRINGOTOMY, "surgery myringotomy"),
        (ENT_TREATMENT_SURGERY_CERUMEN_REMOVAL, "surgery cerumen removal"),
        (ENT_TREATMENT_SURGERY_GRANULOMA_REMOVAL, "surgery granuloma removal"),
        (ENT_TREATMENT_SURGERY_SEPTORHINOPLASTY, "surgery septorhinoplasty"),
        (ENT_TREATMENT_SURGERY_SCAR_REVISION_CLEFT_LIP, "surgery scar revision cleft"),
        (ENT_TREATMENT_SURGERY_FRENULECTOMY, "surgery frenulectomy"),
        (ENT_TREATMENT_OTHER, "other")
    )

    treatment = models.CharField(max_length = 1, choices = ENT_TREATMENT_CHOICES, default = ENT_TREATMENT_OTHER)

    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_NONE = 'n'
    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"), (EAR_SIDE_NONE, "none"))

    side = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    '''
    If treatment == ENT_TREATMENT_OTHER, comment holds mandatory details of 
    the treatment which is not among the possible choices. Otherwise, comment 
    contains an optional comment for the specified treatment.
    '''

    comment = models.TextField(default = "")
