#(C) Copyright Syd Logan 2019-2020
#(C) Copyright Thousand Smiles Foundation 2019-2020
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
unit tests for ent exam application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateENTExam(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTExam, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entexam/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setNormal(self, val):
        self._payload["normal"] = val 
        self.setPayload(self._payload)
    
    def setMicrotia(self, val):
        self._payload["microtia"] = val 
        self.setPayload(self._payload)
    
    def setWax(self, val):
        self._payload["wax"] = val 
        self.setPayload(self._payload)
    
    def setDrainage(self, val):
        self._payload["drainage"] = val 
        self.setPayload(self._payload)
    
    def setExternalOtitis(self, val):
        self._payload["externalOtitis"] = val 
        self.setPayload(self._payload)
    
    def setFb(self, val):
        self._payload["fb"] = val 
        self.setPayload(self._payload)
    
    def setTubeRight(self, val):
        self._payload["tubeRight"] = val 
        self.setPayload(self._payload)
    
    def setTubeLeft(self, val):
        self._payload["tubeLeft"] = val 
        self.setPayload(self._payload)
    
    def setTympanoLeft(self, val):
        self._payload["tympanoLeft"] = val 
        self.setPayload(self._payload)
    
    def setTympanoRight(self, val):
        self._payload["tympanoRight"] = val 
        self.setPayload(self._payload)
    
    def setTmGranulations(self, val):
        self._payload["tmGranulations"] = val 
        self.setPayload(self._payload)
    
    def setTmRetraction(self, val):
        self._payload["tmRetraction"] = val 
        self.setPayload(self._payload)
    
    def setTmAtelectasis(self, val):
        self._payload["tmAtelectasis"] = val 
        self.setPayload(self._payload)
    
    def setPerfRight(self, val):
        self._payload["perfRight"] = val 
        self.setPayload(self._payload)
    
    def setPerfLeft(self, val):
        self._payload["perfLeft"] = val 
        self.setPayload(self._payload)
    
    def setVoiceTest(self, val):
        self._payload["voiceTest"] = val 
        self.setPayload(self._payload)
    
    def setForkAD(self, val):
        self._payload["forkAD"] = val 
        self.setPayload(self._payload)
    
    def setForkAS(self, val):
        self._payload["forkAS"] = val 
        self.setPayload(self._payload)
    
    def setBc(self, val):
        self._payload["bc"] = val 
        self.setPayload(self._payload)
    
    def setFork(self, val):
        self._payload["fork"] = val 
        self.setPayload(self._payload)
    
    def setComment(self, val):
        self._payload["comment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
    
class GetENTExam(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/entexam/{}/".format(self._id)
        else:
            base = "tscharts/v1/entexam/"

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
        super(GetENTExam, self).__init__()
        
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

class UpdateENTExam(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTExam, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entexam/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setNormal(self, val):
        self._payload["normal"] = val 
        self.setPayload(self._payload)
    
    def setMicrotia(self, val):
        self._payload["microtia"] = val 
        self.setPayload(self._payload)
    
    def setWax(self, val):
        self._payload["wax"] = val 
        self.setPayload(self._payload)
    
    def setDrainage(self, val):
        self._payload["drianage"] = val 
        self.setPayload(self._payload)
    
    def setExternalOtitis(self, val):
        self._payload["externalOtitis"] = val 
        self.setPayload(self._payload)
    
    def setFb(self, val):
        self._payload["fb"] = val 
        self.setPayload(self._payload)
    
    def setTubeRight(self, val):
        self._payload["tubeRight"] = val 
        self.setPayload(self._payload)
    
    def setTubeLeft(self, val):
        self._payload["tubeLeft"] = val 
        self.setPayload(self._payload)
    
    def setTympanoLeft(self, val):
        self._payload["tympanoLeft"] = val 
        self.setPayload(self._payload)
    
    def setTympanoRight(self, val):
        self._payload["tympanoRight"] = val 
        self.setPayload(self._payload)
    
    def setTmGranulations(self, val):
        self._payload["tmGranulations"] = val 
        self.setPayload(self._payload)
    
    def setTmRetraction(self, val):
        self._payload["tmRetraction"] = val 
        self.setPayload(self._payload)
    
    def setTmAtelectasis(self, val):
        self._payload["tmAtelectasis"] = val 
        self.setPayload(self._payload)
    
    def setPerfRight(self, val):
        self._payload["perfRight"] = val 
        self.setPayload(self._payload)
    
    def setPerfLeft(self, val):
        self._payload["perfLeft"] = val 
        self.setPayload(self._payload)
    
    def setVoiceTest(self, val):
        self._payload["voiceTest"] = val 
        self.setPayload(self._payload)
    
    def setForkAD(self, val):
        self._payload["forkAD"] = val 
        self.setPayload(self._payload)
    
    def setForkAS(self, val):
        self._payload["forkAS"] = val 
        self.setPayload(self._payload)
    
    def setBc(self, val):
        self._payload["bc"] = val 
        self.setPayload(self._payload)
    
    def setFork(self, val):
        self._payload["fork"] = val 
        self.setPayload(self._payload)
    
    def setComment(self, val):
        self._payload["comment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
class DeleteENTExam(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTExam, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/entexam/{}/".format(id))

class TestTSENTExam(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTExam(self):
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

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTExam(host, port, token)
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

        keys = ["clinic", "time", "patient", "username",
                "normal", "microtia", "wax", "drainage",
                "externalOtitis", "fb", "tubeLeft", 
                "tubeRight", "tympanoLeft", "tympanoRight", 
                "tmGranulations", "tmRetraction", "tmAtelectasis",
                "perfRight", "perfLeft", "voiceTest", "forkAS",
                "forkAD", "bc", "fork", "comment"]

        for x in keys:
            self.assertTrue(x in data)

        self.assertEqual(data["patient"], patientid)
        self.assertEqual(data["clinic"], clinicid)
        self.assertEqual(data["normal"], "left")
        self.assertEqual(data["microtia"], "right")
        self.assertEqual(data["wax"], "both")
        self.assertEqual(data["drainage"], "none")
        self.assertEqual(data["externalOtitis"], "left")
        self.assertEqual(data["fb"], "none")
        self.assertEqual(data["tubeLeft"], "in place")
        self.assertEqual(data["tubeRight"], "extruding")
        self.assertEqual(data["tympanoLeft"], "posterior")
        self.assertEqual(data["tympanoRight"], "50 percent")
        self.assertEqual(data["tmGranulations"], "left")
        self.assertEqual(data["tmRetraction"], "right")
        self.assertEqual(data["tmAtelectasis"], "both")
        self.assertEqual(data["perfLeft"], "posterior")
        self.assertEqual(data["perfRight"], "50 percent")
        self.assertEqual(data["voiceTest"], "normal")
        self.assertEqual(data["forkAD"], "a greater b")
        self.assertEqual(data["forkAS"], "a equal b")
        self.assertEqual(data["bc"], "ad lat ad")
        self.assertEqual(data["fork"], "512")
        self.assertEqual(data["comment"], "A comment")
        self.assertEqual(data["username"], "Gomez")

        x = DeleteENTExam(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTExam(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTExam(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTExam(host, port, token)
        x.setClinic("abcd")
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateENTExam(host, port, token)
        x.setClinic(clinicid)
        x.setPatient("abcd")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteENTExam(self):
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

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTExam(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTExam(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTExam(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTExam(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTExam(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTExam(self):
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

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTExam(host, port, token, id)
        x.setBc("ad lat as")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["bc"] == "ad lat as")

        x = UpdateENTExam(host, port, token, id)
        x.setNormal("left")
        x.setForkAD("a greater b")
        x.setFork("512")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setPerfRight("zzz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setNormal(123)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setMicrotia(14)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setForkAD(999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setPerfRight("total")
        x.setFork(513)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTExam(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setPerfRight("total")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["normal"] == "left")
        self.assertTrue(ret[1]["forkAD"] == "a greater b")
        self.assertTrue(ret[1]["fork"] == "512")
        self.assertTrue(ret[1]["perfRight"] == "total")

        x = UpdateENTExam(host, port, token, id)
        x.setVoiceTest("abnormal")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTExam(host, port, token, id)
        x.setTympanoRight("total")
        x.setTympanoLeft("25 percent")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["normal"] == "left")
        self.assertTrue(ret[1]["forkAD"] == "a greater b")
        self.assertTrue(ret[1]["fork"] == "512")
        self.assertTrue(ret[1]["perfRight"] == "total")
        self.assertTrue(ret[1]["voiceTest"] == "abnormal")
        self.assertTrue(ret[1]["tympanoLeft"] == "25 percent")
        self.assertTrue(ret[1]["tympanoRight"] == "total")

        x = DeleteENTExam(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTExams(self):
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

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        x.setComment("A comment")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTExam(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setNormal("left")
        x.setMicrotia("right")
        x.setWax("both")
        x.setDrainage("none")
        x.setExternalOtitis("left")
        x.setFb("none")
        x.setTubeLeft("in place")
        x.setTubeRight("extruding")
        x.setTympanoLeft("posterior")
        x.setTympanoRight("50 percent")
        x.setTmGranulations("left")
        x.setTmRetraction("right")
        x.setTmAtelectasis("both")
        x.setPerfLeft("posterior")
        x.setPerfRight("50 percent")
        x.setVoiceTest("normal")
        x.setForkAD("a greater b")
        x.setForkAS("a equal b")
        x.setBc("ad lat ad")
        x.setFork("512")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTExam(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTExam(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTExam(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTExam(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTExam(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTExam(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTExam(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTExam(host, port, token)
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
    print("entexam [-h host] [-p port] [-u username] [-w password]") 

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
