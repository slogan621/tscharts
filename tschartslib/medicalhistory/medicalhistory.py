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
unit tests for medical history application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateMedicalHistory(ServiceAPI):
    def __init__(self, host, port, token, clinic, patient):
        super(CreateMedicalHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {"patient": patient, "clinic": clinic}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/medicalhistory/")

    def setMedicalHistory(self, history):
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)
    
class GetMedicalHistory(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/medicalhistory/{}/".format(self._id)
        else:
            base = "tscharts/v1/medicalhistory/"

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
        super(GetMedicalHistory, self).__init__()
        
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

class UpdateMedicalHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateMedicalHistory, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/medicalhistory/{}/".format(id))

    def setMedicalHistory(self, history):
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class DeleteMedicalHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteMedicalHistory, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/medicalhistory/{}/".format(id))

class TestTSMedicalHistory(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateMedicalHistory(self):
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

        x = CreateMedicalHistory(host, port, token, patient=patientid, clinic=clinicid)
       
        data = {}
        data["cold_cough_fever"] = False
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 9
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x.setMedicalHistory(data)
 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetMedicalHistory(host, port, token)
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

        self.assertTrue("cold_cough_fever" in data)
        self.assertTrue("hivaids" in data)
        self.assertTrue("anemia" in data)
        self.assertTrue("athsma" in data)
        self.assertTrue("cancer" in data)
        self.assertTrue("congenitalheartdefect" in data)
        self.assertTrue("congenitalheartdefect_workup" in data)
        self.assertTrue("congenitalheartdefect_planforcare" in data)
        self.assertTrue("diabetes" in data)
        self.assertTrue("epilepsy" in data)
        self.assertTrue("bleeding_problems" in data)
        self.assertTrue("hepititis" in data)
        self.assertTrue("tuberculosis" in data)
        self.assertTrue("troublespeaking" in data)
        self.assertTrue("troublehearing" in data)
        self.assertTrue("troubleeating" in data)
        self.assertTrue("pregnancy_duration" in data)
        self.assertTrue("pregnancy_smoke" in data)
        self.assertTrue("birth_complications" in data)
        self.assertTrue("pregnancy_complications" in data)
        self.assertTrue("mother_alcohol" in data)
        self.assertTrue("relative_cleft" in data)
        self.assertTrue("parents_cleft" in data)
        self.assertTrue("siblings_cleft" in data)
        self.assertTrue("meds" in data)
        self.assertTrue("allergymeds" in data)
        self.assertTrue("first_crawl" in data)
        self.assertTrue("first_sit" in data)
        self.assertTrue("first_walk" in data)
        self.assertTrue("first_words" in data)
        self.assertTrue("birth_weight" in data)
        self.assertTrue("weight" in data)
        self.assertTrue("height" in data)

        self.assertTrue(data["cold_cough_fever"] == False)
        self.assertTrue(data["hivaids"] == False)
        self.assertTrue(data["anemia"] == False)
        self.assertTrue(data["athsma"] == False)
        self.assertTrue(data["cancer"] == False)
        self.assertTrue(data["congenitalheartdefect"] == False)
        self.assertTrue(data["congenitalheartdefect_workup"] == False)
        self.assertTrue(data["congenitalheartdefect_planforcare"] == False)
        self.assertTrue(data["diabetes"] == False)
        self.assertTrue(data["epilepsy"] == False)
        self.assertTrue(data["bleeding_problems"] == False)
        self.assertTrue(data["hepititis"] == False)
        self.assertTrue(data["tuberculosis"] == False)
        self.assertTrue(data["troublespeaking"] == False)
        self.assertTrue(data["troublehearing"] == False)
        self.assertTrue(data["troubleeating"] == False)
        self.assertTrue(data["pregnancy_duration"] == 9)
        self.assertTrue(data["pregnancy_smoke"] == False)
        self.assertTrue(data["birth_complications"] == False)
        self.assertTrue(data["pregnancy_complications"] == False)
        self.assertTrue(data["mother_alcohol"] == False)
        self.assertTrue(data["relative_cleft"] == False)
        self.assertTrue(data["parents_cleft"] == False)
        self.assertTrue(data["siblings_cleft"] == False)
        self.assertTrue(data["meds"] == "")
        self.assertTrue(data["allergymeds"] == "")
        self.assertTrue(data["first_crawl"] == 8)
        self.assertTrue(data["first_sit"] == 7)
        self.assertTrue(data["first_walk"] == 13)
        self.assertTrue(data["first_words"] == 11)
        self.assertTrue(data["birth_weight"] == 3)
        self.assertTrue(data["height"] == 61)
        self.assertTrue(data["weight"] == 9)

        x = GetMedicalHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data = ret[1]

        self.assertTrue("cold_cough_fever" in data)
        self.assertTrue("hivaids" in data)
        self.assertTrue("anemia" in data)
        self.assertTrue("athsma" in data)
        self.assertTrue("cancer" in data)
        self.assertTrue("congenitalheartdefect" in data)
        self.assertTrue("congenitalheartdefect_workup" in data)
        self.assertTrue("congenitalheartdefect_planforcare" in data)
        self.assertTrue("diabetes" in data)
        self.assertTrue("epilepsy" in data)
        self.assertTrue("bleeding_problems" in data)
        self.assertTrue("hepititis" in data)
        self.assertTrue("tuberculosis" in data)
        self.assertTrue("troublespeaking" in data)
        self.assertTrue("troublehearing" in data)
        self.assertTrue("troubleeating" in data)
        self.assertTrue("pregnancy_duration" in data)
        self.assertTrue("pregnancy_smoke" in data)
        self.assertTrue("birth_complications" in data)
        self.assertTrue("pregnancy_complications" in data)
        self.assertTrue("mother_alcohol" in data)
        self.assertTrue("relative_cleft" in data)
        self.assertTrue("parents_cleft" in data)
        self.assertTrue("siblings_cleft" in data)
        self.assertTrue("meds" in data)
        self.assertTrue("allergymeds" in data)
        self.assertTrue("first_crawl" in data)
        self.assertTrue("first_sit" in data)
        self.assertTrue("first_walk" in data)
        self.assertTrue("first_words" in data)
        self.assertTrue("birth_weight" in data)
        self.assertTrue("weight" in data)
        self.assertTrue("height" in data)

        self.assertTrue(data["cold_cough_fever"] == False)
        self.assertTrue(data["hivaids"] == False)
        self.assertTrue(data["anemia"] == False)
        self.assertTrue(data["athsma"] == False)
        self.assertTrue(data["cancer"] == False)
        self.assertTrue(data["congenitalheartdefect"] == False)
        self.assertTrue(data["congenitalheartdefect_workup"] == False)
        self.assertTrue(data["congenitalheartdefect_planforcare"] == False)
        self.assertTrue(data["diabetes"] == False)
        self.assertTrue(data["epilepsy"] == False)
        self.assertTrue(data["bleeding_problems"] == False)
        self.assertTrue(data["hepititis"] == False)
        self.assertTrue(data["tuberculosis"] == False)
        self.assertTrue(data["troublespeaking"] == False)
        self.assertTrue(data["troublehearing"] == False)
        self.assertTrue(data["troubleeating"] == False)
        self.assertTrue(data["pregnancy_duration"] == 9)
        self.assertTrue(data["pregnancy_smoke"] == False)
        self.assertTrue(data["birth_complications"] == False)
        self.assertTrue(data["pregnancy_complications"] == False)
        self.assertTrue(data["mother_alcohol"] == False)
        self.assertTrue(data["relative_cleft"] == False)
        self.assertTrue(data["parents_cleft"] == False)
        self.assertTrue(data["siblings_cleft"] == False)
        self.assertTrue(data["meds"] == "")
        self.assertTrue(data["allergymeds"] == "")
        self.assertTrue(data["first_crawl"] == 8)
        self.assertTrue(data["first_sit"] == 7)
        self.assertTrue(data["first_walk"] == 13)
        self.assertTrue(data["first_words"] == 11)
        self.assertTrue(data["birth_weight"] == 3)
        self.assertTrue(data["height"] == 61)
        self.assertTrue(data["weight"] == 9)

        x = DeleteMedicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetMedicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateMedicalHistory(host, port, token, clinic=9999, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateMedicalHistory(host, port, token, clinic=clinicid, patient=9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateMedicalHistory(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data, boolean arg

        data = {}
        data["cold_cough_fever"] = 9999    # this should cause a failure
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 9
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x.setMedicalHistory(data)

        x = CreateMedicalHistory(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        #invalid data, pregnancy duration

        data = {}
        data["cold_cough_fever"] = False
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 99
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x.setMedicalHistory(data)

        x = CreateMedicalHistory(host, port, token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteMedicalHistory(self):
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

        x = CreateMedicalHistory(host, port, token, patient=patientid, clinic=clinicid)
        data = {}
        data["cold_cough_fever"] = False
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 9
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x.setMedicalHistory(data)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteMedicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetMedicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteMedicalHistory(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteMedicalHistory(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteMedicalHistory(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteMedicalHistory(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateMedicalHistory(self):
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

        x = CreateMedicalHistory(host, port, token, patient=patientid, clinic=clinicid)
        data = {}
        data["cold_cough_fever"] = False
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 9
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetMedicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        data = {}
        data["siblings_cleft"] = True
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetMedicalHistory(host, port, token)
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
        self.assertTrue("cold_cough_fever" in data)
        self.assertTrue("hivaids" in data)
        self.assertTrue("anemia" in data)
        self.assertTrue("athsma" in data)
        self.assertTrue("cancer" in data)
        self.assertTrue("congenitalheartdefect" in data)
        self.assertTrue("congenitalheartdefect_workup" in data)
        self.assertTrue("congenitalheartdefect_planforcare" in data)
        self.assertTrue("diabetes" in data)
        self.assertTrue("epilepsy" in data)
        self.assertTrue("bleeding_problems" in data)
        self.assertTrue("hepititis" in data)
        self.assertTrue("tuberculosis" in data)
        self.assertTrue("troublespeaking" in data)
        self.assertTrue("troublehearing" in data)
        self.assertTrue("troubleeating" in data)
        self.assertTrue("pregnancy_duration" in data)
        self.assertTrue("pregnancy_smoke" in data)
        self.assertTrue("birth_complications" in data)
        self.assertTrue("pregnancy_complications" in data)
        self.assertTrue("mother_alcohol" in data)
        self.assertTrue("relative_cleft" in data)
        self.assertTrue("parents_cleft" in data)
        self.assertTrue("siblings_cleft" in data)
        self.assertTrue("meds" in data)
        self.assertTrue("allergymeds" in data)
        self.assertTrue(data["siblings_cleft"] == True)
        self.assertTrue(data["first_crawl"] == 8)
        self.assertTrue(data["first_sit"] == 7)
        self.assertTrue(data["first_walk"] == 13)
        self.assertTrue(data["first_words"] == 11)
        self.assertTrue(data["birth_weight"] == 3)
        self.assertTrue(data["height"] == 61)
        self.assertTrue(data["weight"] == 9)

        data = {}
        data["hepititis"] = True 
        data["pregnancy_duration"] = 8 
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetMedicalHistory(host, port, token)
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
        self.assertTrue("cold_cough_fever" in data)
        self.assertTrue("hivaids" in data)
        self.assertTrue("anemia" in data)
        self.assertTrue("athsma" in data)
        self.assertTrue("cancer" in data)
        self.assertTrue("congenitalheartdefect" in data)
        self.assertTrue("congenitalheartdefect_workup" in data)
        self.assertTrue("congenitalheartdefect_planforcare" in data)
        self.assertTrue("diabetes" in data)
        self.assertTrue("epilepsy" in data)
        self.assertTrue("bleeding_problems" in data)
        self.assertTrue("hepititis" in data)
        self.assertTrue("tuberculosis" in data)
        self.assertTrue("troublespeaking" in data)
        self.assertTrue("troublehearing" in data)
        self.assertTrue("troubleeating" in data)
        self.assertTrue("pregnancy_duration" in data)
        self.assertTrue("pregnancy_smoke" in data)
        self.assertTrue("birth_complications" in data)
        self.assertTrue("pregnancy_complications" in data)
        self.assertTrue("mother_alcohol" in data)
        self.assertTrue("relative_cleft" in data)
        self.assertTrue("parents_cleft" in data)
        self.assertTrue("siblings_cleft" in data)
        self.assertTrue("meds" in data)
        self.assertTrue("allergymeds" in data)
        self.assertTrue(data["hepititis"] == True)
        self.assertTrue(data["pregnancy_duration"] == 8)
        self.assertTrue(data["parents_cleft"] == True) 
        self.assertTrue(data["first_crawl"] == 8)
        self.assertTrue(data["first_sit"] == 7)
        self.assertTrue(data["first_walk"] == 13)
        self.assertTrue(data["first_words"] == 11)
        self.assertTrue(data["birth_weight"] == 3)
        self.assertTrue(data["height"] == 61)
        self.assertTrue(data["weight"] == 9)

        data = {}
        data["hepititis"] = "Hello" 
        data["pregnancy_duration"] = 8 
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = None
        data["pregnancy_duration"] = 8 
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = False 
        data["pregnancy_duration"] = 3 
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = True
        data["allergymeds"] = 56
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = "Poor"
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["hepititis"] = None
        data["parents_cleft"] = True 
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        data = {}
        x = UpdateMedicalHistory(host, port, token, id)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)   # ok to update nothing

        x = DeleteMedicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllMedicalHistories(self):
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

        data = {}
        data["cold_cough_fever"] = False
        data["hivaids"] = False
        data["anemia"] = False
        data["athsma"] = False
        data["cancer"] = False
        data["congenitalheartdefect"] = False
        data["congenitalheartdefect_workup"] = False
        data["congenitalheartdefect_planforcare"] = False
        data["diabetes"] = False
        data["epilepsy"] = False
        data["bleeding_problems"] = False
        data["hepititis"] = False
        data["tuberculosis"] = False
        data["troublespeaking"] = False
        data["troublehearing"] = False
        data["troubleeating"] = False
        data["pregnancy_duration"] = 9
        data["pregnancy_smoke"] = False
        data["birth_complications"] = False
        data["pregnancy_complications"] = False
        data["mother_alcohol"] = False
        data["relative_cleft"] = False
        data["parents_cleft"] = False
        data["siblings_cleft"] = False
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = 8
        data["first_sit"] = 7
        data["first_walk"] = 13
        data["first_words"] = 11 
        data["birth_weight"] = 3
        data["height"] = 61
        data["weight"] = 9
        data["birth_weight_metric"] = True
        data["height_metric"] = True
        data["weight_metric"] = True

        x = CreateMedicalHistory(host, port, token, patient=patientid1, clinic=clinicid1)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid2, clinic=clinicid1)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid3, clinic=clinicid1)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid1, clinic=clinicid2)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid2, clinic=clinicid2)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid3, clinic=clinicid2)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid1, clinic=clinicid3)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid2, clinic=clinicid3)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateMedicalHistory(host, port, token, patient=patientid3, clinic=clinicid3)
        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetMedicalHistory(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetMedicalHistory(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetMedicalHistory(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetMedicalHistory(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetMedicalHistory(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetMedicalHistory(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteMedicalHistory(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetMedicalHistory(host, port, token)
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
    print("medicalhistory [-h host] [-p port] [-u username] [-w password]") 

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
