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
unit tests for the register application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json
import time

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateRegistration(ServiceAPI):
    def __init__(self, host, port, token, clinic, patient):
        super(CreateRegistration, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {"patient": patient, "clinic": clinic}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/register/")

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)

class GetRegistration(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetRegistration, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        if id:
            self.setURL("tscharts/v1/register/{}".format(id))
        else:
            self.setURL("tscharts/v1/register/")
    
    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)

    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)

class UpdateRegistration(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateRegistration, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/register/{}/".format(id))

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)

class DeleteRegistration(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteRegistration, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/register/{}/".format(id))

class GetAllRegistrations(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllRegistrations, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/register/")

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)

    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)

class TestTSRegistration(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateRegistration(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data = ret[1]

        self.assertTrue("timein" in data)
        self.assertTrue("timeout" in data)
        self.assertTrue("state" in data)
        self.assertTrue(data["state"] == "Checked In")

        x = DeleteRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateRegistration(host, port, token, clinic=9999, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateRegistration(host, port, token, clinic=clinicid, patient=9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # invalid state

        x = CreateRegistration(host, port, token, clinic=clinicid, patient=patientid)
        x.setState("foo")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateRegistration(host, port, token, clinic=clinicid, patient=patientid)
        x.setState("")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateRegistration(host, port, token, clinic=clinicid, patient=patientid)
        x.setState(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteRegistration(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteRegistration(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteRegistration(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteRegistration(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteRegistration(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateRegistration(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateRegistration(host, port, token, id)
        x.setState("Checked In")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data = ret[1]
        self.assertTrue("state" in data)
        self.assertTrue(data["state"] == "Checked In")

        x = UpdateRegistration(host, port, token, id)
        x.setState("Checked Out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data = ret[1]
        self.assertTrue("state" in data)
        self.assertTrue(data["state"] == "Checked Out")

        x = UpdateRegistration(host, port, token, id)
        x.setState("foo")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateRegistration(host, port, token, id)
        x.setState({})
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateRegistration(host, port, token, id)
        x.setState(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)   

        x = UpdateRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)  

        x = DeleteRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateStateTimestamps(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        self.assertTrue("timein" in ret[1])
        timein = ret[1]["timein"]
        self.assertTrue("timeout" in ret[1])
        timeout = ret[1]["timeout"]
        self.assertTrue(timein == timeout)
        timeintmp = timein
        timeouttmp = timein

        time.sleep(5)

        x = UpdateRegistration(host, port, token, id)
        x.setState("Checked In")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data = ret[1]
        self.assertTrue("state" in data)
        self.assertTrue(data["state"] == "Checked In")

        self.assertTrue("timein" in ret[1])
        timein = ret[1]["timein"]
        self.assertTrue("timeout" in ret[1])
        timeout = ret[1]["timeout"]

        self.assertTrue(timeout == timeouttmp) 
        self.assertTrue(timein > timeintmp) 
        timeintmp = timein

        time.sleep(5)

        x = UpdateRegistration(host, port, token, id)
        x.setState("Checked Out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data = ret[1]
        self.assertTrue("state" in data)
        self.assertTrue(data["state"] == "Checked Out")

        self.assertTrue("timein" in ret[1])
        timein = ret[1]["timein"]
        self.assertTrue("timeout" in ret[1])
        timeout = ret[1]["timeout"]

        self.assertTrue(not timeout == timeouttmp) 
        self.assertTrue(timein == timeintmp) 
        self.assertTrue(timeout > timein) 

        x = DeleteRegistration(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)


    def testGetAllRegistrations(self):
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
        data["gender"] = "Male"
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

        x = CreateRegistration(host, port, token, patient=patientid1, clinic=clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid2, clinic=clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid3, clinic=clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid1, clinic=clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid2, clinic=clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid3, clinic=clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid1, clinic=clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid2, clinic=clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid3, clinic=clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetAllRegistrations(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetAllRegistrations(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetAllRegistrations(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetAllRegistrations(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetAllRegistrations(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetAllRegistrations(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteRegistration(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetAllRegistrations(host, port, token)
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
    print("register [-h host] [-p port] [-u username] [-w password]") 

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
