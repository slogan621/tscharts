#(C) Copyright Syd Logan 2019-2021
#(C) Copyright Thousand Smiles Foundation 2019-2021
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

class ENTExam(models.Model):
    clinic = models.ForeignKey(Clinic)
    patient = models.ForeignKey(Patient)
    username = models.CharField(max_length=64, default = "")  # user supplied name
    time = models.DateTimeField(auto_now=True)

    EAR_SIDE_LEFT = 'l'
    EAR_SIDE_RIGHT = 'r'
    EAR_SIDE_BOTH = 'b'
    EAR_SIDE_NONE = 'n'
    EAR_SIDE_CHOICES = ((EAR_SIDE_LEFT, "left"), (EAR_SIDE_RIGHT, "right"), (EAR_SIDE_BOTH, "both"), (EAR_SIDE_NONE, "none"))

    normal = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    microtia = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    wax = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    drainage = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    externalOtitis = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    fb = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    ENT_TUBE_IN_PLACE = 'p'
    ENT_TUBE_EXTRUDING = 'e'
    ENT_TUBE_IN_CANAL = 'c'
    ENT_TUBE_NONE = 'n'

    ENT_TUBE_CHOICES = ((ENT_TUBE_IN_PLACE, 'in place'), (ENT_TUBE_EXTRUDING, 'extruding'), (ENT_TUBE_IN_CANAL, 'in canal'), (ENT_TUBE_NONE, 'none'))

    tubeRight = models.CharField(max_length = 1, choices = ENT_TUBE_CHOICES, default = ENT_TUBE_NONE)
    tubeLeft = models.CharField(max_length = 1, choices = ENT_TUBE_CHOICES, default = ENT_TUBE_NONE)

    ENT_TYMPANOSCLEROSIS_ANTERIOR = 'a'
    ENT_TYMPANOSCLEROSIS_POSTERIOR = 'p'
    ENT_TYMPANOSCLEROSIS_25 = '2'
    ENT_TYMPANOSCLEROSIS_50 = '5'
    ENT_TYMPANOSCLEROSIS_75 = '7'
    ENT_TYMPANOSCLEROSIS_TOTAL = 't'
    ENT_TYMPANOSCLEROSIS_NONE = 'n'

    ENT_TYMPANOSCLEROSIS_CHOICES = ((ENT_TYMPANOSCLEROSIS_ANTERIOR, 'anterior'), (ENT_TYMPANOSCLEROSIS_POSTERIOR, 'posterior'), (ENT_TYMPANOSCLEROSIS_25, '25 percent'), (ENT_TYMPANOSCLEROSIS_50, '50 percent'), (ENT_TYMPANOSCLEROSIS_75, '75 percent'), (ENT_TYMPANOSCLEROSIS_TOTAL, 'total'), (ENT_TYMPANOSCLEROSIS_NONE, 'none'))

    tympanoRight = models.CharField(max_length = 1, choices = ENT_TYMPANOSCLEROSIS_CHOICES, default = ENT_TYMPANOSCLEROSIS_NONE)
    tympanoLeft = models.CharField(max_length = 1, choices = ENT_TYMPANOSCLEROSIS_CHOICES, default = ENT_TYMPANOSCLEROSIS_NONE)

    tmGranulations = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tmRetraction = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    tmAtelectasis = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    ENT_PERF_ANTERIOR = 'a'
    ENT_PERF_POSTERIOR = 'p'
    ENT_PERF_MARGINAL = 'm'
    ENT_PERF_25 = '2'
    ENT_PERF_50 = '5'
    ENT_PERF_75 = '7'
    ENT_PERF_TOTAL = 't'
    ENT_PERF_NONE = 'n'

    ENT_PERF_CHOICES = ((ENT_PERF_ANTERIOR, 'anterior'), (ENT_PERF_POSTERIOR, 'posterior'), (ENT_PERF_MARGINAL, 'marginal'), (ENT_PERF_25, '25 percent'), (ENT_PERF_50, '50 percent'), (ENT_PERF_75, '75 percent'), (ENT_PERF_TOTAL, 'total'), (ENT_PERF_NONE, 'none'))

    perfRight = models.CharField(max_length = 1, choices = ENT_PERF_CHOICES, default = ENT_PERF_NONE)
    perfLeft = models.CharField(max_length = 1, choices = ENT_PERF_CHOICES, default = ENT_PERF_NONE)

    ENT_VOICE_TEST_NORMAL = 'n'
    ENT_VOICE_TEST_ABNORMAL = 'a'
    ENT_VOICE_TEST_NONE = 'o'

    ENT_VOICE_TEST_CHOICES = ((ENT_VOICE_TEST_NORMAL, 'normal'), (ENT_VOICE_TEST_ABNORMAL, 'abnormal'), (ENT_VOICE_TEST_NONE, 'none'))

    voiceTest = models.CharField(max_length = 1, choices = ENT_VOICE_TEST_CHOICES, default = ENT_VOICE_TEST_NONE)

    ENT_FORK_TEST_A_GREATER_B = 'a'
    ENT_FORK_TEST_B_GREATER_A = 'b'
    ENT_FORK_TEST_EQUAL = 'e'
    ENT_FORK_TEST_NONE = 'n'

    ENT_FORK_TEST_CHOICES = ((ENT_FORK_TEST_A_GREATER_B, 'a greater b'), (ENT_FORK_TEST_B_GREATER_A, 'b greater a'), (ENT_FORK_TEST_EQUAL, 'a equal b'), (ENT_FORK_TEST_NONE, 'none'))

    forkAD = models.CharField(max_length = 1, choices = ENT_FORK_TEST_CHOICES, default = ENT_FORK_TEST_NONE)
    forkAS = models.CharField(max_length = 1, choices = ENT_FORK_TEST_CHOICES, default = ENT_FORK_TEST_NONE)

    ENT_BC_AD_LAT_TO_AD = 'a'
    ENT_BC_AD_LAT_TO_AS = 'b'
    ENT_BC_AS_LAT_TO_AD = 'c'
    ENT_BC_AS_LAT_TO_AS = 'd'
    ENT_BC_NONE = 'n'

    ENT_BC_CHOICES = ((ENT_BC_AD_LAT_TO_AD, 'ad lat ad'), (ENT_BC_AD_LAT_TO_AS, 'ad lat as'), (ENT_BC_AS_LAT_TO_AD, 'as lat ad'), (ENT_BC_AS_LAT_TO_AS, 'as lat as'), (ENT_BC_NONE, 'none'))

    bc = models.CharField(max_length = 1, choices = ENT_BC_CHOICES, default = ENT_BC_AD_LAT_TO_AD)

    ENT_FORK_256 = '2'
    ENT_FORK_512 = '5'
    ENT_FORK_NONE = 'n'

    ENT_FORK_CHOICES = ((ENT_FORK_256, '256'), (ENT_FORK_512, '512'), (ENT_FORK_NONE, 'none'))

    fork = models.CharField(max_length = 1, choices = ENT_FORK_CHOICES, default = ENT_FORK_NONE)

    comment = models.TextField(default = "")
    effusion = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)
    middle_ear_infection = models.CharField(max_length = 1, choices = EAR_SIDE_CHOICES, default = EAR_SIDE_NONE)

    # support yes, no, n/a (not applicable) options
    EAR_TRI_STATE_BOOLEAN_YES = 'y'
    EAR_TRI_STATE_BOOLEAN_NO = 'n'
    EAR_TRI_STATE_BOOLEAN_NA = 'a' # not applicable
    EAR_TRI_STATE_BOOLEAN_CHOICES = ((EAR_TRI_STATE_BOOLEAN_NA, "na"), (EAR_TRI_STATE_BOOLEAN_YES, "yes"), (EAR_TRI_STATE_BOOLEAN_NO, "no"))

    cleft_lip = models.BooleanField(default = False)
    cleft_palate = models.BooleanField(default = False)
    repaired_lip = models.CharField(max_length = 1, choices = EAR_TRI_STATE_BOOLEAN_CHOICES, default = EAR_TRI_STATE_BOOLEAN_NA)
    repaired_palate = models.CharField(max_length = 1, choices = EAR_TRI_STATE_BOOLEAN_CHOICES, default = EAR_TRI_STATE_BOOLEAN_NA)
