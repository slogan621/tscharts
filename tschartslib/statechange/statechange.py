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
unit tests for statechange application. Assumes django server is up
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

class CreateStateChange(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateStateChange, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/statechange/")

    def setClinicStation(self, clinic_station):
        self._payload["clinicstation"] = clinic_station
        self.setPayload(self._payload)
    
    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)
    
class GetStateChange(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/statechange/{}/".format(self._id)
        else:
            base = "tscharts/v1/statechange/".format(self._id)

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._clinicstation == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinicstation={}".format(self._clinicstation)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token, id=None):
        super(GetStateChange, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.clearArgs()
        self.makeURL()

    def clearArgs(self):
        self._patient = None
        self._clinic = None
        self._clinicstation = None
        self._id = None

    def setClinicStation(self, clinic_station):
        self._clinicstation = clinic_station
        self.makeURL()
    
    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()
    
    def setPatient(self, patient):
        self._patient = patient
        self.makeURL()

    def setId(self, id):
        self._id = id
        self.makeURL()

class DeleteStateChange(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteStateChange, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/statechange/{}/".format(id))

class TestTSStateChange(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateStateChange(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        statechangeid = int(ret[1]["id"])

        x = GetStateChange(host, port, token)
        x.setId(statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == statechangeid)
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("time" in ret[1]);
        self.assertTrue("state" in ret[1]);
        self.assertTrue(ret[1]["state"] == "in");

        x = DeleteStateChange(host, port, token, statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

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

    # create with invalid clinicstation

    def testCreateStateChangeBadClinicStation(self):

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(9999)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # create with invalid patient

    def testCreateStateChangeBadPatient(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(9999)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
 
        # create with invalid state

    def testCreateStateChangeBadState(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("new york")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

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
 
 
        # create multiple, verify they all exist and are correct

    def testCreateMultipleStateChange(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        statechangeid = int(ret[1]["id"])

        x = GetStateChange(host, port, token)
        x.setId(statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == statechangeid)
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("time" in ret[1]);
        self.assertTrue("state" in ret[1]);
        self.assertTrue(ret[1]["state"] == "in");

        x = DeleteStateChange(host, port, token, statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

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
 
    def testDeleteStateChange(self):

        # create statechange, delete, verify it is gone

        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        statechangeid = int(ret[1]["id"])

        x = GetStateChange(host, port, token)
        x.setId(statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == statechangeid)
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("time" in ret[1]);
        self.assertTrue("state" in ret[1]);
        self.assertTrue(ret[1]["state"] == "in");

        x = DeleteStateChange(host, port, token, statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # try deleting an invalid state change

        x = DeleteStateChange(host, port, token, statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # create a few state change objects, delete them
        # and verify there are none in the database

        ids = []
        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        for x in ids:
            y = GetStateChange(host, port, token)
            y.setId(x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == x)

        for x in ids:
            y = DeleteStateChange(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in ids:
            y = GetStateChange(host, port, token)
            y.setId(x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 404)

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

    def testGetAllStateChange(self):

        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

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

        x = CreateStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        x.setState("in")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        statechangeid = int(ret[1]["id"])

        x = GetStateChange(host, port, token)
        x.setId(statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == statechangeid)
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("time" in ret[1]);
        self.assertTrue("state" in ret[1]);
        self.assertTrue(ret[1]["state"] == "in");

        # following tests assume that there is only one matching statechange 
        # in the DB. Note these forms of the GET return vectors, not a single
        # object

        x = GetStateChange(host, port, token)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1][0] 
        self.assertTrue("id" in ret)
        self.assertTrue(int(ret["id"]) == statechangeid)
        self.assertTrue(int(ret["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret["patient"] == patientid))
        self.assertTrue("time" in ret);
        self.assertTrue("state" in ret);
        self.assertTrue(ret["state"] == "in");

        x.clearArgs()
        x.setClinicStation(clinicstationid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1][0] 
        self.assertTrue("id" in ret)
        self.assertTrue(int(ret["id"]) == statechangeid)
        self.assertTrue(int(ret["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret["patient"] == patientid))
        self.assertTrue("time" in ret);
        self.assertTrue("state" in ret);
        self.assertTrue(ret["state"] == "in");

        x.clearArgs()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1][0] 
        self.assertTrue("id" in ret)
        self.assertTrue(int(ret["id"]) == statechangeid)
        self.assertTrue(int(ret["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret["patient"] == patientid))
        self.assertTrue("time" in ret);
        self.assertTrue("state" in ret);
        self.assertTrue(ret["state"] == "in");

        x.clearArgs()
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1][0] 
        self.assertTrue("id" in ret)
        self.assertTrue(int(ret["id"]) == statechangeid)
        self.assertTrue(int(ret["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret["patient"] == patientid))
        self.assertTrue("time" in ret);
        self.assertTrue("state" in ret);
        self.assertTrue(ret["state"] == "in");

        x.clearArgs()
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1][0] 
        self.assertTrue("id" in ret)
        self.assertTrue(int(ret["id"]) == statechangeid)
        self.assertTrue(int(ret["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret["patient"] == patientid))
        self.assertTrue("time" in ret);
        self.assertTrue("state" in ret);
        self.assertTrue(ret["state"] == "in");

        x = DeleteStateChange(host, port, token, statechangeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

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

def usage():
    print("statechange [-h host] [-p port] [-u username] [-w password]") 

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
