#(C) Copyright Syd Logan 2017-2019
#(C) Copyright Thousand Smiles Foundation 2017-2019
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
from station.models import Station
from clinicstation.models import ClinicStation
from routingslip.models import RoutingSlip
from routingslip.models import RoutingSlipEntry
import datetime

# data about all queues in clinic

class QueueStatus(models.Model):
    clinic = models.ForeignKey(Clinic)
    numwaiting = models.IntegerField()
    minq = models.IntegerField()
    maxq = models.IntegerField()
    avgq = models.IntegerField()
    minwait = models.TimeField(default=datetime.time(0,0))
    maxwait = models.TimeField(default=datetime.time(0,0))
    avgwait = models.TimeField(default=datetime.time(0,0))

# a specific queue 

class Queue(models.Model):
    clinic = models.ForeignKey(Clinic) 
    station = models.ForeignKey(Station) 
    clinicstation = models.ForeignKey(ClinicStation) 
    avgservicetime = models.TimeField(default=datetime.time(0,0))

# a specific queue entry

class QueueEntry(models.Model):
    queue = models.ForeignKey(Queue)
    patient = models.ForeignKey(Patient)
    timein = models.DateTimeField()
    waittime = models.TimeField(default=datetime.time(0,0)) # timenow - timein
    routingslip = models.ForeignKey(RoutingSlip)
    routingslipentry = models.ForeignKey(RoutingSlipEntry)
    estwaittime = models.TimeField(default=datetime.time(0,0)) # queue average service time * (number of patients ahead of this patient in the queue)
