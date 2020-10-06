#(C) Copyright Syd Logan 2018-2020
#(C) Copyright Thousand Smiles Foundation 2018-2020
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
unit tests for returntoclinicstation application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.station.station import CreateStation, DeleteStation
from tschartslib.clinicstation.clinicstation import CreateClinicStation, DeleteClinicStation

class CreateReturnToClinicStation(ServiceAPI):
    def __init__(self, host, port, token, clinic, patient, station, requestingclinicstation):
        super(CreateReturnToClinicStation, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"clinic": clinic, "patient": patient, "station": station, "requestingclinicstation": requestingclinicstation}
        self.setPayload(payload)
        self.setURL("tscharts/v1/returntoclinicstation/")
    
class GetReturnToClinicStation(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/returntoclinicstation/{}/".format(self._id)
        else:
            base = "tscharts/v1/returntoclinicstation/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._state == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "state={}".format(self._state)
            hasQArgs = True

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        if not self._station == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "station={}".format(self._station)
            hasQArgs = True

        if not self._requestingclinicstation == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "requestingclinicstation={}".format(self._requestingclinicstation)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetReturnToClinicStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._station = None
        self._patient = None
        self._requestingclinicstation = None
        self._state = None
        self._id = None
        self.makeURL()

    def setId(self, id):
        self._id = id;
        self.makeURL()
    
    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setStation(self, station):
        self._station = station
        self.makeURL()

    def setPatient(self, patient):
        self._patient = patient
        self.makeURL()

    def setState(self, state):
        self._state = state
        self.makeURL()

    def setRequestingClinicStation(self, requestingclinicstation):
        self._requestingclinicstation = requestingclinicstation
        self.makeURL()

class UpdateReturnToClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateReturnToClinicStation, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/returntoclinicstation/{}/".format(id))

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)

class DeleteReturnToClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteReturnToClinicStation, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/returntoclinicstation/{}/".format(id))

class TestTSReturnToClinicStation(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateReturnToClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid = int(ret[1]["id"])

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=clinicid, station=stationid, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        requestingclinicstationId = int(ret[1]["requestingclinicstation"])
        self.assertTrue(requestingclinicstationId == requestingclinicstationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("state" in ret[1])
        self.assertTrue(ret[1]["state"] == "created")

        x = DeleteReturnToClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=9999, station=stationid, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=clinicid, station=9999, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent requestingclinicstation param

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=clinicid, station=stationid, requestingclinicstation=9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateReturnToClinicStation(host, port, token, patient=9999, clinic=clinicid, station=stationid, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinicStation(host, port, token, requestingclinicstationid)
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

    def testDeleteReturnToClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid = int(ret[1]["id"])

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=clinicid, station=stationid, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteReturnToClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteReturnToClinicStation(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinicStation(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinicStation(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinicStation(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # cleanup

        x = DeleteClinicStation(host, port, token, requestingclinicstationid)
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

    def testUpdateReturnToClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid = int(ret[1]["id"])

        x = CreateReturnToClinicStation(host, port, token, patient=patientid, clinic=clinicid, station=stationid, requestingclinicstation=requestingclinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("requestingclinicstation" in ret[1])
        clinicstationId = int(ret[1]["requestingclinicstation"])
        self.assertTrue(clinicstationId == requestingclinicstationid)

        x = UpdateReturnToClinicStation(host, port, token, id)
        x.setState("scheduled_dest")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("state" in ret[1])
        self.assertTrue(ret[1]["state"] == "scheduled_dest")

        x = UpdateReturnToClinicStation(host, port, token, id)
        x.setState("checked_out_dest")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("state" in ret[1])
        self.assertTrue(ret[1]["state"] == "checked_out_dest")

        x = UpdateReturnToClinicStation(host, port, token, id)
        x.setState("scheduled_return")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinicStation(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("state" in ret[1])
        self.assertTrue(ret[1]["state"] == "scheduled_return")

        x = UpdateReturnToClinicStation(host, port, token, id)
        x.setState("foo")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateReturnToClinicStation(host, port, token, id)
        x.setState("")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateReturnToClinicStation(host, port, token, 9999)
        x.setState("scheduled_dest")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, requestingclinicstationid)
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

    def testGetAllReturnToClinicStations(self):
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
        patientid1 = int(ret[1]["id"])

        data["paternal_last"] = "bbcd1234"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data["paternal_last"] = "cbcd1234"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test1")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid1 = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid2 = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test3")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        requestingclinicstationid3 = int(ret[1]["id"])

        ids = []
        delids = []

        # 3 different patients, 
        # 3 different requesting clinicstations = 9 combinations

        for aPatient in [patientid1, patientid2, patientid3]:
            for aRequestingClinicStation in [requestingclinicstationid1, requestingclinicstationid2, requestingclinicstationid3]:
 
                x = CreateReturnToClinicStation(host, port, token, patient=aPatient, clinic=clinicid, station=stationid, requestingclinicstation=aRequestingClinicStation)
                ret = x.send(timeout=30)
                self.assertEqual(ret[0], 200)
                ids.append(int(ret[1]["id"]))
                delids.append(int(ret[1]["id"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertEqual(len(rtcs), 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(patientid1 == int(ret[1]["patient"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertEqual(len(rtcs), 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(patientid2 == int(ret[1]["patient"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertEqual(len(rtcs), 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(patientid3 == int(ret[1]["patient"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 9)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(stationid == int(ret[1]["station"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setRequestingClinicStation(requestingclinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(requestingclinicstationid1 == int(ret[1]["requestingclinicstation"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setRequestingClinicStation(requestingclinicstationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(requestingclinicstationid2 == int(ret[1]["requestingclinicstation"]))

        x = GetReturnToClinicStation(host, port, token)
        x.setStation(stationid)
        x.setRequestingClinicStation(requestingclinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)
        for x in rtcs:
            y = GetReturnToClinicStation(host, port, token)
            y.setId(int(x["id"]))
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue(stationid == int(ret[1]["station"]))
            self.assertTrue(requestingclinicstationid1 == int(ret[1]["requestingclinicstation"]))

        x = GetReturnToClinicStation(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 9)

        for x in rtcs:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to find all created returntoclinicstation items {}".format(ids) == None)

        for x in delids:
            y = DeleteReturnToClinicStation(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetReturnToClinicStation(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetReturnToClinicStation(host, port, token)
        x.setClinic(stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetReturnToClinicStation(host, port, token)
        x.setRequestingClinicStation(requestingclinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetReturnToClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = DeleteClinicStation(host, port, token, requestingclinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, requestingclinicstationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, requestingclinicstationid3)
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
    print("returntoclinicstation [-h host] [-p port] [-u username] [-w password]") 

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
