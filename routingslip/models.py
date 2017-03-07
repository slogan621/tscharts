from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from clinic.models import Clinic
from patient.models import Patient
from clinicstation.models import ClinicStation 

'''
Routing slip identifies the patient, the clinic, and category of patient.
The category may change from clinic to clinic based on care given.
'''

class RoutingSlip(models.Model):
    patient = models.ForeignKey(Patient)
    clinic = models.ForeignKey(Clinic)
    NEWCLEFT = 'n'
    DENTAL = 'd'
    RETCLEFT = 'r'
    ORTHO = 'o'
    OTHER = 't'
    UNKNOWN = 'u'
    CATEGORY_CHOICES = ((NEWCLEFT, "New Cleft"), 
                        (DENTAL, "Dental"),
                        (RETCLEFT, "Returning Cleft"),
                        (ORTHO, "Ortho"),
                        (OTHER, "Other"),
                        (UNKNOWN, "Unknown"),)

    category = models.CharField(
        max_length = 1,
        choices = CATEGORY_CHOICES,
        default = OTHER,
    )

'''
A given patient will be associated with a routing slip and a set of 
stations that he or she must visit. A record in this table defines
one such station and its order of visitation. Its order may change
during the clinic. Routing slip entries can be added or removed to
the routing slip during the patient stay. The initial set is defined
by the patient classification (e.g., dental patients only need to be
routed to dental). A specialist can add, remove, or change the 
relative order of items in the routing slip. When an item is added
to the routing slip, its state is SCHEDULED. Removal does not result
in the record being deleted from the database, it is just a state 
change REMOVED. Once a patient has visited a station, the routing 
slip entry is marked VISITED.
'''
 
class RoutingSlipEntry(models.Model):
    routingslip = models.ForeignKey(RoutingSlip)
    clinicstation = models.ForeignKey(ClinicStation)
    order = models.IntegerField(default=0)   
    SCHEDULED = 'a'   # checkin to station is pending (or clinic ended)
    VISITED = 'v'     # patient was checked in at the station
    REMOVED = 'r'     # entry was removed by someone before seen by station
    STATE_CHOICES = ((SCHEDULED, "Scheduled"), 
                     (VISITED, "Visited"),
                     (REMOVED, "Removed"),)

    state = models.CharField(
        max_length = 1,
        choices = STATE_CHOICES,
        default = SCHEDULED,
    )

class RoutingSlipComment(models.Model):
    routingslip = models.ForeignKey(RoutingSlip)
    comment = models.TextField()
    author = models.ForeignKey(User)    # logged in user that added the comment
    updatetime = models.DateTimeField(auto_now=True)
