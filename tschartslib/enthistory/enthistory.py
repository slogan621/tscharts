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

'''
unit tests for ent history application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateENTHistory(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enthistory/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setPainDuration(self, val):
        self._payload["painDuration"] = val 
        self.setPayload(self._payload)
    
    def setPainSide(self, val):
        self._payload["painSide"] = val 
        self.setPayload(self._payload)
    
    def setHearingLossDuration(self, val):
        self._payload["hearingLossDuration"] = val 
        self.setPayload(self._payload)
    
    def setHearingLossSide(self, val):
        self._payload["hearingLossSide"] = val 
        self.setPayload(self._payload)
    
    def setDrainageDuration(self, val):
        self._payload["drainageDuration"] = val 
        self.setPayload(self._payload)
    
    def setDrainageSide(self, val):
        self._payload["drainageSide"] = val 
        self.setPayload(self._payload)
    
    def setComment(self, val):
        self._payload["comment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
    
class GetENTHistory(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/enthistory/{}/".format(self._id)
        else:
            base = "tscharts/v1/enthistory/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetENTHistory, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._patient = None
        self._id = None
        self.makeURL()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setPatient(self, patient):
        self._patient = patient
        self.makeURL()

    def setPainSide(self, val):
        self._painSide = val
        self.makeURL()

    def setPainDuration(self, val):
        self._painuration = val
        self.makeURL()

    def setHearingLossSide(self, val):
        self._hearingLossSide = val
        self.makeURL()

    def setHearingLossDuration(self, val):
        self._hearingLossDuration = val
        self.makeURL()

    def setDrainageSide(self, val):
        self._drainageSide = val
        self.makeURL()

    def setDrainageDuration(self, val):
        self._drainageDuration = val
        self.makeURL()

class UpdateENTHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTHistory, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enthistory/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setPainDuration(self, val):
        self._payload["painDuration"] = val
        self.setPayload(self._payload)

    def setPainSide(self, val):
        self._payload["painSide"] = val
        self.setPayload(self._payload)

    def setHearingLossDuration(self, val):
        self._payload["hearingLossDuration"] = val
        self.setPayload(self._payload)

    def setHearingLossSide(self, val):
        self._payload["hearingLossSide"] = val
        self.setPayload(self._payload)

    def setDrainageDuration(self, val):
        self._payload["drainageDuration"] = val
        self.setPayload(self._payload)

    def setDrainageSide(self, val):
        self._payload["drainageSide"] = val
        self.setPayload(self._payload)

    def setComment(self, val):
        self._payload["comment"] = val
        self.setPayload(self._payload)

    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)

class DeleteENTHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTHistory, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/enthistory/{}/".format(id))

class TestTSENTHistory(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTHistory(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data = ret[1]

        self.assertTrue("painSide" in data)
        self.assertTrue(data["painSide"] == "right")
        self.assertTrue("painDuration" in data)
        self.assertTrue(data["painDuration"] == "weeks")
        self.assertTrue("hearingLossSide" in data)
        self.assertTrue(data["hearingLossSide"] == "right")
        self.assertTrue("hearingLossDuration" in data)
        self.assertTrue(data["hearingLossDuration"] == "weeks")
        self.assertTrue("drainageSide" in data)
        self.assertTrue(data["drainageSide"] == "right")
        self.assertTrue("drainageDuration" in data)
        self.assertTrue(data["drainageDuration"] == "weeks")
        self.assertTrue("comment" in data)
        self.assertTrue(data["comment"] == "A comment")
        self.assertTrue("username" in data)
        self.assertTrue(data["username"] == "Gomez")

        x = DeleteENTHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTHistory(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTHistory(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateENTHistory(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTHistory(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setDrainageDuration("17")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x.setHearingLossSide("oooo")
        x.setHearingLossDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x.setPainSide("left")
        x.setPainDuration("jjjj")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
      
        # missing username 
        x = CreateENTHistory(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteENTHistory(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTHistory(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistory(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistory(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTHistory(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTHistory(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTHistory(host, port, token, id)
        x.setHearingLossDuration("none")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["hearingLossDuration"] == "none")

        x = UpdateENTHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setHearingLossSide("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["hearingLossSide"] == "both")

        x = UpdateENTHistory(host, port, token, id)
        x.setPainSide("zzz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTHistory(host, port, token, id)
        x.setDrainageDuration("weeks")
        x.setDrainageSide("yadda")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTHistories(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid1 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "05/05/2016", "05/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid2 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "08/05/2016", "08/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid3 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "3abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid1 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "1abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "2abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        delids = []

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTHistory(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTHistory(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTHistory(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTHistory(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTHistory(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTHistory(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTHistory(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTHistory(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = DeleteClinic(host, port, token, clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("enthistory [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    global host
    host = "127.0.0.1"
    global port
    port = 8000
    global username
    username = None
    global password
    password = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
