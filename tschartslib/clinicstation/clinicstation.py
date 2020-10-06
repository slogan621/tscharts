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
unit tests for clinic station application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.station.station import CreateStation, DeleteStation
from tschartslib.patient.patient import CreatePatient, GetPatient, DeletePatient

class CreateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, clinic, station, active=False, away=True, finished=False, name="", name_es="", level=None):
        super(CreateClinicStation, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"clinic": clinic, "away": away, "station": station, "active": active, "name": name, "finished": finished, "name_es": name_es, "level": level}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/")
    
class GetClinicStation(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/clinicstation/{}/".format(self._id)
        else:
            base = "tscharts/v1/clinicstation/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._active == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "active={}".format(self._active)
            hasQArgs = True

        if not self._level == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "level={}".format(self._level)
            hasQArgs = True

        if not self._away == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "away={}".format(self._away)
            hasQArgs = True

        if not self._finished == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "finished={}".format(self._finished)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token, id=None):
        super(GetClinicStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._id = None
        self._away = None
        self._active = None
        self._finished = None
        self._level = None
        self._clinic = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setAway(self, away):
        self._away = away
        self.makeURL()

    def setFinished(self, finished):
        self._finished = finished
        self.makeURL()

    def setActive(self, active):
        self._active = active
        self.makeURL()

    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setLevel(self, level):
        self._level = level
        self.makeURL()

class UpdateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateClinicStation, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

    def setAway(self, away):
        self._payload["away"] = away
        self.setPayload(self._payload)

    def setFinished(self, finished):
        self._payload["finished"] = finished
        self.setPayload(self._payload)

    def setActive(self, active):
        self._payload["active"] = active
        self.setPayload(self._payload)

    def setName(self, name):
        self._payload["name"] = name
        self.setPayload(self._payload)

    def setNameES(self, name):
        self._payload["name_es"] = name
        self.setPayload(self._payload)

    def setLevel(self, level):
        self._payload["level"] = level
        self.setPayload(self._payload)

    def setActivePatient(self, patient):
        self._payload["activepatient"] = patient
        self.setPayload(self._payload)

    def setNextPatient(self, patient):
        self._payload["nextpatient"] = patient
        self.setPayload(self._payload)

    def setAwayTime(self, minutes):
        self._payload["awaytime"] = minutes
        self.setPayload(self._payload)

class DeleteClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteClinicStation, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

class TestTSClinicStation(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        # default active and away state 

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test1")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "test1")

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit active state

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=False, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "test2")
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "")
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit away state

        x = CreateClinicStation(host, port, token, clinicid, stationid, away=False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == False)
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, away=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)
        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit finished state

        x = CreateClinicStation(host, port, token, clinicid, stationid, finished=False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("finished" in ret[1])
        self.assertTrue(ret[1]["finished"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, finished=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["finished"] == True)
        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateClinicStation(host, port, token, 9999, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateClinicStation(host, port, token, clinicid, 9999, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # bogus active param

        x = CreateClinicStation(host, port, token, clinicid, stationid, active="Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # bogus away param

        x = CreateClinicStation(host, port, token, clinicid, stationid, away="Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testNextAndActivePatient(self):
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
        x = GetPatient(host, port, token)
        x.setId(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True) 
        self.assertTrue("name" in ret[1])
        self.assertTrue("name_es" in ret[1])
        self.assertTrue(ret[1]["name"] == "") 
        self.assertTrue(ret[1]["name_es"] == "") 
        self.assertTrue(ret[1]["activepatient"] == None)
        self.assertTrue(ret[1]["nextpatient"] == None)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(False)
        x.setAway(True)
        x.setAwayTime(15)
        x.setName("Dental 1")
        x.setActivePatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 15)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Dental 1")
        self.assertTrue("willreturn" in ret[1])
        self.assertTrue(ret[1]["activepatient"] == patientid)
        self.assertTrue(ret[1]["nextpatient"] == None)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(True)
        x.setAway(False)
        x.setActivePatient(None)
        x.setNextPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)
        self.assertTrue(ret[1]["activepatient"] == None)
        self.assertTrue(ret[1]["nextpatient"] == patientid)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(15)
        x.setActivePatient(None)
        x.setNextPatient(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 15)
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)
        self.assertTrue(ret[1]["activepatient"] == None)
        self.assertTrue(ret[1]["nextpatient"] == None)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(0)
        x.setAwayTime(23)
        x.setActive(False)
        x.setAway(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 0)
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 23)
        self.assertTrue("willreturn" in ret[1])
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue(ret[1]["activepatient"] == None)
        self.assertTrue(ret[1]["nextpatient"] == None)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True) 
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "") 

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(False)
        x.setAway(True)
        x.setAwayTime(15)
        x.setName("Dental 1")
        x.setNameES("Dental Uno")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 15)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Dental 1")
        self.assertTrue(ret[1]["name_es"] == "Dental Uno")
        self.assertTrue("willreturn" in ret[1])

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(True)
        x.setAway(False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 15)
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(0)
        x.setAwayTime(23)
        x.setActive(False)
        x.setAway(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 0)
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 23)
        self.assertTrue("willreturn" in ret[1])
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllClinicStations(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        entstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        dentalstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Ortho")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        orthostationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Screening")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        screeningstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Speech")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        speechstationid = int(ret[1]["id"])

        ids = []
        delids = []
        x = CreateClinicStation(host, port, token, clinicid, entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, screeningstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = GetClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stations = ret[1]
        self.assertTrue(len(stations) == 5)
        for x in stations:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to find all created clinicstation items {}".format(ids) == None)

        for x in delids:
            y = DeleteClinicStation(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        stations = ret[1]
        self.assertTrue(len(stations) == 0)

def usage():
    print("clinicstations [-h host] [-p port] [-u username] [-w password]") 

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
