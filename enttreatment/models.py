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

from enthistory.models import ENTHistory

class ENTTreatment(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name

    time = models.DateTimeField(auto_now=True)

    # Ear cleaned [] AD [] AS
    earCleanedSide = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    earCleanedComment = models.TextField(default = "")
    # Audiogram [] AD [] AS [] AU
    audiogramSide = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    audiogramComment = models.TextField(default = "")
    # [] Right away and return to see me right afterwards. May need
    # surgery tomorrow.
    audiogramRightAway = models.BooleanField(default = False)
    audiogramRightAwayComment = models.TextField(default = "")
    # Tympanogram [] AD [] AS [] AU
    tympanogramSide = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    tympanogramComment = models.TextField(default = "")
    # [] Right away and return to see me right afterwards. May need
    # surgery tomorrow.
    tympanogramRightAway = models.BooleanField(default = False)
    tympanogramRightAwayComment = models.TextField(default = "")
    #Mastoid debrided [] AD [] AS [] Hearing aid evaluation
    mastoidDebridedSide = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    mastoidDebridedComment = models.TextField(default = "")
    mastoidDebridedHearingAidEval = models.BooleanField(default = False)
    mastoidDebridedHearingAidEvalComment = models.TextField(default = "")
    #Antibiotic [] drops [] orally [] for acute infection [] for after water exposure infection prevention
    antibioticDrops = models.BooleanField(default = False)
    antibioticDropsComment = models.TextField(default = "")
    antibioticOrally = models.BooleanField(default = False)
    antibioticOrallyComment = models.TextField(default = "")
    antibioticAcuteInfection = models.BooleanField(default = False)
    antibioticAcuteInfectionComment = models.TextField(default = "")
    antibioticAfterWaterExposureInfectionPrevention = models.BooleanField(default = False)
    antibioticAfterWaterExposureInfectionPreventionComment = models.TextField(default = "")
    # Boric acid powder [] instilled today [] dispensed for home use Tube removed [] AD [] AS
    boricAcidToday = models.BooleanField(default = False)
    boricAcidTodayComment = models.TextField(default = "")
    boricAcidForHomeUse = models.BooleanField(default = False)
    boricAcidForHomeUseComment = models.TextField(default = "")
    boricAcidSide = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    boricAcidSideComment = models.TextField(default = "")
    #Foreign body removed [] AD []AS
    foreignBodyRemoved = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    foreignBodyRemovedComment = models.TextField(default = "")
    #Return [] 3 mos [] 6 mos [] prn
    return3Months = models.BooleanField(default = False)
    return6Months = models.BooleanField(default = False)
    returnPrn = models.BooleanField(default = False)
    returnComment = models.TextField(default = "")
    # [] Referred to pvt ENT in Ensenada
    referredPvtENTEnsenada = models.BooleanField(default = False)
    referredPvtENTEnsenadaComment = models.TextField(default = "")
    # [] Referred to Childrens Hospital in Tijuana
    referredChildrensHospitalTJ = models.BooleanField(default = False)
    referredChildrensHospitalTJComment = models.TextField(default = "")

    # tomorrow surgeries

    #Tubes [] AD [] AS [] AU
    tubesTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    tubesTomorrowComment = models.TextField(default = "")
    # T Plasty [] AD [] AS [] AU
    tPlastyTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    tPlastyTomorrowComment = models.TextField(default = "")
    # EUA (Examination under anesthesia) [] AD [] AS [] AU 
    euaTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    euaTomorrowComment = models.TextField(default = "")
    #FB (foreign body) removal [] AD [] AS [] AU
    fbRemovalTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    fbRemovalTomorrowComment = models.TextField(default = "")
    # Middle Ear Exploration via myringotomy [] AD [] AS [] AU 
    middleEarExploreMyringotomyTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    middleEarExploreMyringotomyTomorrowComment = models.TextField(default = "")
    # Cerumen removal [] AD [] AS [] AU
    cerumenTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    cerumenTomorrowComment = models.TextField(default = "")
    # Granuloma removal [] AD [] AS [] AU
    granulomaTomorrow = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    granulomaTomorrowComment = models.TextField(default = "")
    #[] Septorhinoplasty
    septorhinoplastyTomorrow = models.BooleanField(default = False)
    septorhinoplastyTomorrowComment = models.TextField(default = "")
    #[] Scar revision cleft lip
    scarRevisionCleftLipTomorrow = models.BooleanField(default = False)
    scarRevisionCleftLipTomorrowComment = models.TextField(default = "")
    #[] Frenulectomy
    frenulectomyTomorrow = models.BooleanField(default = False)
    frenulectomyTomorrowComment = models.TextField(default = "")

    # future surgeries

    #Tubes [] AD [] AS [] AU
    tubesFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    tubesFutureComment = models.TextField(default = "")
    # T plasty [] AD [] AS [] AU
    tPlastyFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    tPlastyFutureComment = models.TextField(default = "")
    # EUA (Examination under anesthesia) [] AD [] AS [] AU 
    euaFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    euaFutureComment = models.TextField(default = "")
    #FB (foreign body) removal [] AD [] AS [] AU
    fbRemovalFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    fbRemovalFutureComment = models.TextField(default = "")
    # Middle Ear Exploration via myringotomy [] AD [] AS [] AU 
    middleEarExploreMyringotomyFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    middleEarExploreMyringotomyFutureComment = models.TextField(default = "")
    # Cerumen removal [] AD [] AS [] AU
    cerumenFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    cerumenFutureComment = models.TextField(default = "")
    # Granuloma removal [] AD [] AS [] AU
    granulomaFuture = models.CharField(max_length = 1, choices = ENTHistory.EAR_SIDE_CHOICES, default = ENTHistory.EAR_SIDE_BOTH)
    granulomaFutureComment = models.TextField(default = "")
    #[] Septorhinoplasty
    septorhinoplastyFuture = models.BooleanField(default = False)
    septorhinoplastyFutureComment = models.TextField(default = "")
    #[] Scar revision cleft lip
    scarRevisionCleftLipFuture = models.BooleanField(default = False)
    scarRevisionCleftLipFutureComment = models.TextField(default = "")
    #[] Frenulectomy
    frenulectomyFuture = models.BooleanField(default = False)
    frenulectomyFutureComment = models.TextField(default = "")

    comment = models.TextField(default = "")

