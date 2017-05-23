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

'''
A clinic has stations. There are two models: 

Station: simply a named location in the clinic. These records in
the database define the universe of all possible stations that a
clinic can be made up of.

ClinicStation: defines a station for a particular clinic. The 
station can be marked active or inactive. If inactive, then it
can be added to a patient routing slip, but the scheduler will
not route patients to an inactive station (this inactivity might
apply for some part of the day (e.g., the provider is out to 
lunch) or for the entire clinic (in this case, perhaps the station
was deemed important for a patient in the current clinic routing
slip, and since the patient did not get scheduled there, it becomes
a part of the patients' routing slip for the next clinic he or 
she attends).
''' 

class ClinicStation(models.Model):
    name = models.CharField(max_length=64)
    station = models.ForeignKey(Station)
    clinic = models.ForeignKey(Clinic)
    active = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    away = models.BooleanField(default=True)
    awaytime = models.IntegerField(default=30)
    willreturn = models.DateTimeField(auto_now_add=True)
