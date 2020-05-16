#(C) Copyright Syd Logan 2017-2020
#(C) Copyright Thousand Smiles Foundation 2017-2020
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
from django.contrib.auth.models import User

from clinic.models import Clinic
from patient.models import Patient
from station.models import Station 
from returntoclinicstation.models import ReturnToClinicStation 

'''
Routing slip identifies the patient, the clinic, and category of patient.
The category may change from clinic to clinic based on care given.
'''

class RoutingSlip(models.Model):
    patient = models.ForeignKey(Patient)
    clinic = models.ForeignKey(Clinic)
    NEWCLEFT = 'n'
    DENTAL = 'd'
    HEARINGAIDS = 'h'
    EARS = 'e'
    RETCLEFT = 'r'
    ORTHO = 'o'
    OTHER = 't'
    UNKNOWN = 'u'
    CATEGORY_CHOICES = ((NEWCLEFT, "New Cleft"), 
                        (DENTAL, "Dental"),
                        (HEARINGAIDS, "Hearing Aids"), 
                        (EARS, "Ears"),
                        (RETCLEFT, "Returning Cleft"),
                        (ORTHO, "Ortho"),
                        (OTHER, "Other"))

    category = models.CharField(
        max_length = 1,
        choices = CATEGORY_CHOICES,
        default = OTHER,
    )
    createtime = models.DateTimeField(auto_now_add=True)
    statechangetime = models.DateTimeField(auto_now=True)

'''
A given patient will be associated with a routing slip and a set of 
routing slip entries that represent both stations in the clinic the
patient must visit, and the order of visitation.

The order of visitation may change during the clinic based on 
modification by staff at any one of the stations. Routing slip entries 
can be added or removed to the routing slip during the patient stay. 

The initial list of routing slip entries is defined by the patient 
classification (e.g., dental patients will only need to be seen by 
a dentist). This classification is made by assigning the patient a
category at registration. The category can also be changed during a
stay, which will trigger in some way changes to the routing slip.

When an item is added to the routing slip, its state is NEW or RETURN. 
Removal does not result in the record being deleted from the database, 
rather it is just a state change to REMOVED state.

RETURN indicates that a patient has a corresponding returntoclinicstation
resource. This often is used by dentists to send a patient to x-ray and
have that patient return back to the dental chair immediately once the
x-rays are available, but it can be used in other circumstances as well.
'''
 
class RoutingSlipEntry(models.Model):
    routingslip = models.ForeignKey(RoutingSlip)
    station = models.ForeignKey(Station)
    order = models.IntegerField(default=0)   
    NEW = 'n'           # newly created, needs to be placed in a queue
    SCHEDULED = 's'     # is sitting in a queue
    CHECKEDIN = 'i'     # patient was checked in at the station
    CHECKEDOUT = 'o'    # patient was checked in at the station
    REMOVED = 'r'       # entry was removed by someone before seen by station
    RETURN = 'l'        # entry is a return to clinic station entry
    STATE_CHOICES = ((NEW, "New"), 
                     (SCHEDULED, "Scheduled"), 
                     (CHECKEDIN, "Checked In"),
                     (CHECKEDOUT, "Checked Out"),
                     (REMOVED, "Removed"),
                     (REMOVED, "Deleted"),
                     (RETURN, "Return"),)

    state = models.CharField(
        max_length = 1,
        choices = STATE_CHOICES,
        default = NEW,
    )
    returntoclinicstation = models.ForeignKey(ReturnToClinicStation, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    statechangetime = models.DateTimeField(auto_now=True)

class RoutingSlipComment(models.Model):
    routingslip = models.ForeignKey(RoutingSlip)
    comment = models.TextField()
    author = models.ForeignKey(User)    # logged in user that added the comment
    updatetime = models.DateTimeField(auto_now=True)
