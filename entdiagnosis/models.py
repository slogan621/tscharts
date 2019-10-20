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

class ENTDiagnosis(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name
    comment = models.TextField(default = "")
    time = models.DateTimeField(auto_now=True)

    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_NONE = 'n'
    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"), (EAR_SIDE_NONE, "none"))

    # hearing loss

    hlConductive = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    hl = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    hlMixed = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    hlSensory = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    # external ear

    externalCerumenImpaction = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    externalEarCanalFB = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    externalMicrotia = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    # tympanic membrane

    tympanicAtelectasis = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tympanicGranuloma = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tympanicMonomer = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tympanicTube = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tympanicPerf = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    # middle ear

    middleEarCholesteatoma = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    
    # middle ear Eustachian Tube Dysfunction with TM Retraction
    middleEarEustTubeDysTMRetraction = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    middleEarOtitisMedia = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    middleEarSerousOtitisMedia = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    # oral cavity

    oralAnkyloglossia = models.BooleanField(default = False)
    oralTonsilEnlarge = models.BooleanField(default = False)
    oralCleftLipRepairDeformity = models.BooleanField(default = False)
    oralCleftLipUnilateral = models.BooleanField(default = False)
    oralCleftLipBilateral = models.BooleanField(default = False)
    oralCleftLipUnrepaired = models.BooleanField(default = False)
    oralCleftLipRepaired = models.BooleanField(default = False)
    oralCleftPalateUnilateral = models.BooleanField(default = False)
    oralCleftPalateBilateral = models.BooleanField(default = False)
    oralCleftPalateUnrepaired = models.BooleanField(default = False)
    oralCleftPalateRepaired = models.BooleanField(default = False)
    oralSpeechProblem = models.BooleanField(default = False)

    # nose

    noseDeviatedSeptum = models.BooleanField(default = False)
    noseTurbinateHypertrophy = models.BooleanField(default = False)
    noseDeformitySecondaryToCleftPalate = models.BooleanField(default = False)

    # syndrome

    syndromeHemifacialMicrosomia = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    syndromePierreRobin = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
