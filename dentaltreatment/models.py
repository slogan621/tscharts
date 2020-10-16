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

# Treatment completed today

class DentalTreatment(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name

    time = models.DateTimeField(auto_now=True)
    exam = models.BooleanField(default = False)
    examComment = models.TextField(default = "")
    prophy = models.BooleanField(default = False)  # cleaning
    prophyComment = models.TextField(default = "")

    srpUR = models.BooleanField(default = False) 
    srpLR = models.BooleanField(default = False) 
    srpUL = models.BooleanField(default = False) 
    srpLL = models.BooleanField(default = False) 
    srpComment = models.TextField(default = "")

    xraysViewed = models.BooleanField(default = False) 
    xraysViewedComment = models.TextField(default = "")

    headNeckOralCancerExam = models.BooleanField(default = False) 
    headNeckOralCancerExamComment = models.TextField(default = "")

    oralHygieneInstruction = models.BooleanField(default = False) 
    oralHygieneInstructionComment = models.TextField(default = "")

    flourideTxVarnish = models.BooleanField(default = False) 
    flourideTxVarnishComment = models.TextField(default = "")

    nutritionalCounseling = models.BooleanField(default = False) 
    nutritionalCounselingComment = models.TextField(default = "")

    orthoEvaluation = models.BooleanField(default = False) 
    orthoEvaluationComment = models.TextField(default = "")
    orthoTx = models.BooleanField(default = False) 
    orthoTxComment = models.TextField(default = "")

    oralSurgeryEvaluation = models.BooleanField(default = False) 
    oralSurgeryEvaluationComment = models.TextField(default = "")
    oralSurgeryTx = models.BooleanField(default = False) 
    oralSurgeryTxComment = models.TextField(default = "")

    DENTAL_ANESTHETIC_NONE = 'n'
    DENTAL_ANESTHETIC_BENZOCAINE_TOPICAL = 'b'
    DENTAL_ANESTHETIC_LIDOCAINE = 'l'    
    DENTAL_ANESTHETIC_SEPTOCAINE = 's'    
    DENTAL_ANESTHETIC_OTHER = 'o'    

    DENTAL_ANESTHETIC_CHOICES = ((DENTAL_ANESTHETIC_NONE, "none"), (DENTAL_ANESTHETIC_BENZOCAINE_TOPICAL, "benzocaine"), (DENTAL_ANESTHETIC_LIDOCAINE, "lidocaine"), (DENTAL_ANESTHETIC_SEPTOCAINE, "septocaine"), (DENTAL_ANESTHETIC_OTHER, "other"))

    localAnesthetic = models.CharField(max_length = 1, choices = DENTAL_ANESTHETIC_CHOICES, default = DENTAL_ANESTHETIC_NONE)
    localAnestheticNumberCarps = models.IntegerField(default = 0)
    localAnestheticComment = models.TextField(default = "")

    comment = models.TextField(default = "")

