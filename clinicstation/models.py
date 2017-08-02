#(C) Copyright Syd Logan 2016
#(C) Copyright Thousand Smiles Foundation 2016
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

from clinic.models import Clinic
from station.models import Station
from patient.models import Patient

'''
A clinic has stations. There are two models: 

Station: simply a named location in the clinic. These records in
the database define the universe of all possible stations that a
clinic can be made up of. A station represents a class.

ClinicStation: defines an actual station for a particular clinic. 
The station can be marked active or inactive. If inactive, it is
currently not seeing a patient, and the activepatient field 
should be set to null (or None in Python). If active is True,
then the activepatient field should contain the ID of the patient
currently being seen. The station can "checkout" the activepatient
and that will cause the activepatient field to be set to NULL, 
and the active field to be set to False.

The nextpatient field contains the ID of the next patient to be
seen by a station. When the station is not active, this patient
can be "checked in". When the patient is checked in, the station's
active field is set to True, and the activepatient field will be
assigned the nextpatient value. Then, nextpatient will be set to
the id of the patient next in the queue for this station.

away, awaytime, and willreturn are all used to indicate if the
station is currently manned (or not, perhaps the doctor is at
lunch).  

''' 

class ClinicStation(models.Model):
    name = models.CharField(max_length=64)
    station = models.ForeignKey(Station)
    clinic = models.ForeignKey(Clinic)
    active = models.BooleanField(default=False) # set to True if a patient is being seen
    level = models.IntegerField(default=1) # relative importance to scheduler
    away = models.BooleanField(default=True)  # set to True when station is out to lunch
    awaytime = models.IntegerField(default=30) # default minutes when station goes to away state before clinic is returned to (informational only) 
    willreturn = models.DateTimeField(auto_now_add=True) # estimated time of returen, computed when away is set to True, using the awaytime value
    activepatient = models.ForeignKey(Patient, null=True, related_name='nextpatient') # if active, patient of null
    nextpatient = models.ForeignKey(Patient, null=True, related_name="activepatient") # next patient to be seen or null
    name_es = models.CharField(max_length=64)
