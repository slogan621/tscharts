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

class CreateENTSurgicalHistory(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTSurgicalHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entsurgicalhistory/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setGranuloma(self, val):
        self._payload["granuloma"] = val 
        self.setPayload(self._payload)
    
    def setGranulomaComment(self, val):
        self._payload["granulomacomment"] = val 
        self.setPayload(self._payload)
    
    def setTubes(self, val):
        self._payload["tubes"] = val 
        self.setPayload(self._payload)
    
    def setTubesComment(self, val):
        self._payload["tubescomment"] = val 
        self.setPayload(self._payload)
    
    def setTplasty(self, val):
        self._payload["tplasty"] = val 
        self.setPayload(self._payload)
    
    def setTplastyComment(self, val):
        self._payload["tplastycomment"] = val 
        self.setPayload(self._payload)
    
    def setEua(self, val):
        self._payload["eua"] = val 
        self.setPayload(self._payload)
    
    def setEuaComment(self, val):
        self._payload["euacomment"] = val 
        self.setPayload(self._payload)
    
    def setFb(self, val):
        self._payload["fb"] = val 
        self.setPayload(self._payload)
    
    def setFbComment(self, val):
        self._payload["fbcomment"] = val 
        self.setPayload(self._payload)
    
    def setMyringotomy(self, val):
        self._payload["myringotomy"] = val 
        self.setPayload(self._payload)
    
    def setMyringotomyComment(self, val):
        self._payload["myringotomycomment"] = val 
        self.setPayload(self._payload)
    
    def setCerumen(self, val):
        self._payload["cerumen"] = val 
        self.setPayload(self._payload)
    
    def setCerumenComment(self, val):
        self._payload["cerumencomment"] = val 
        self.setPayload(self._payload)
    
    def setSeptorhinoplasty(self, val):
        self._payload["septorhinoplasty"] = val 
        self.setPayload(self._payload)
    
    def setSeptorhinoplastyComment(self, val):
        self._payload["septorhinoplastycomment"] = val 
        self.setPayload(self._payload)
    
    def setScarrevision(self, val):
        self._payload["scarrevision"] = val 
        self.setPayload(self._payload)
    
    def setScarrevisionComment(self, val):
        self._payload["scarrevisioncomment"] = val 
        self.setPayload(self._payload)
    
    def setFrenulectomy(self, val):
        self._payload["frenulectomy"] = val 
        self.setPayload(self._payload)
    
    def setFrenulectomyComment(self, val):
        self._payload["frenulectomycomment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
    
class GetENTSurgicalHistory(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/entsurgicalhistory/{}/".format(self._id)
        else:
            base = "tscharts/v1/entsurgicalhistory/"

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
        super(GetENTSurgicalHistory, self).__init__()
        
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

class UpdateENTSurgicalHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTSurgicalHistory, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entsurgicalhistory/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setGranuloma(self, val):
        self._payload["granuloma"] = val 
        self.setPayload(self._payload)
    
    def setGranulomaComment(self, val):
        self._payload["granulomacomment"] = val 
        self.setPayload(self._payload)
    
    def setTubes(self, val):
        self._payload["tubes"] = val 
        self.setPayload(self._payload)
    
    def setTubesComment(self, val):
        self._payload["tubescomment"] = val 
        self.setPayload(self._payload)
    
    def setTplasty(self, val):
        self._payload["tplasty"] = val 
        self.setPayload(self._payload)
    
    def setTplastyComment(self, val):
        self._payload["tplastycomment"] = val 
        self.setPayload(self._payload)
    
    def setEua(self, val):
        self._payload["eua"] = val 
        self.setPayload(self._payload)
    
    def setEuaComment(self, val):
        self._payload["euacomment"] = val 
        self.setPayload(self._payload)
    
    def setFb(self, val):
        self._payload["fb"] = val 
        self.setPayload(self._payload)
    
    def setFbComment(self, val):
        self._payload["fbcomment"] = val 
        self.setPayload(self._payload)
    
    def setMyringotomy(self, val):
        self._payload["myringotomy"] = val 
        self.setPayload(self._payload)
    
    def setMyringotomyComment(self, val):
        self._payload["myringotomycomment"] = val 
        self.setPayload(self._payload)
    
    def setCerumen(self, val):
        self._payload["cerumen"] = val 
        self.setPayload(self._payload)
    
    def setCerumenComment(self, val):
        self._payload["cerumencomment"] = val 
        self.setPayload(self._payload)
    
    def setSeptorhinoplasty(self, val):
        self._payload["septorhinoplasty"] = val 
        self.setPayload(self._payload)
    
    def setSeptorhinoplastyComment(self, val):
        self._payload["septorhinoplastycomment"] = val 
        self.setPayload(self._payload)
    
    def setScarrevision(self, val):
        self._payload["scarrevision"] = val 
        self.setPayload(self._payload)
    
    def setScarrevisionComment(self, val):
        self._payload["scarrevisioncomment"] = val 
        self.setPayload(self._payload)
    
    def setFrenulectomy(self, val):
        self._payload["frenulectomy"] = val 
        self.setPayload(self._payload)
    
    def setFrenulectomyComment(self, val):
        self._payload["frenulectomycomment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
    
class DeleteENTSurgicalHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTSurgicalHistory, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/entsurgicalhistory/{}/".format(id))

class TestTSENTSurgicalHistory(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTSurgicalHistory(self):
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

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTSurgicalHistory(host, port, token)
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
                "tubes", "tubescomment", "tplasty", "tplastycomment",
                "eua", "euacomment", "fb", "fbcomment", "myringotomy",
                "myringotomycomment", "cerumen", "cerumencomment", 
                "septorhinoplasty", "septorhinoplastycomment", "scarrevision",
                "scarrevisioncomment", "frenulectomy", "frenulectomycomment"]

        for x in keys:
            self.assertTrue(x in data)

        self.assertEqual(data["patient"], patientid)
        self.assertEqual(data["clinic"], clinicid)
        self.assertEqual(data["username"], "Gomez")
        self.assertEqual(data["tubes"], "left")
        self.assertEqual(data["tubescomment"], "tubes")
        self.assertEqual(data["tplasty"], "right")
        self.assertEqual(data["tplastycomment"], "tplasty")
        self.assertEqual(data["eua"], "both")
        self.assertEqual(data["euacomment"], "eua")
        self.assertEqual(data["fb"], "none")
        self.assertEqual(data["fbcomment"], "fb")
        self.assertEqual(data["myringotomy"], "left")
        self.assertEqual(data["myringotomycomment"], "myring")
        self.assertEqual(data["cerumen"], "right")
        self.assertEqual(data["cerumencomment"], "cerumen")
        self.assertEqual(data["septorhinoplasty"], True)
        self.assertEqual(data["septorhinoplastycomment"], "septo")
        self.assertEqual(data["scarrevision"], False)
        self.assertEqual(data["scarrevisioncomment"], "scar")
        self.assertEqual(data["frenulectomy"], True)
        self.assertEqual(data["frenulectomycomment"], "fren")

        x = DeleteENTSurgicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTSurgicalHistory(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTSurgicalHistory(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTSurgicalHistory(host, port, token)
        x.setClinic("abcd")
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateENTSurgicalHistory(host, port, token)
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

    def testDeleteENTSurgicalHistory(self):
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

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTSurgicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTSurgicalHistory(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTSurgicalHistory(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTSurgicalHistory(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTSurgicalHistory(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTSurgicalHistory(self):
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

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setFb("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["fb"] == "both")

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setFrenulectomy(False)
        x.setTubes("right")
        x.setEua("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setMyringotomy("zzz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setTubes(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCerumenComment(14)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setFrenulectomy("none")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setTplasty("both")
        x.setTubesComment(513)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setScarrevision(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["fb"] == "both")
        self.assertTrue(ret[1]["frenulectomy"] == False)
        self.assertTrue(ret[1]["tubes"] == "right")
        self.assertTrue(ret[1]["eua"] == "both")
        self.assertTrue(ret[1]["scarrevision"] == True)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setTplastyComment("a tplasty comment")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTSurgicalHistory(host, port, token, id)
        x.setCerumen("none")
        x.setFb("left")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["fb"] == "left")
        self.assertTrue(ret[1]["frenulectomy"] == False)
        self.assertTrue(ret[1]["tubes"] == "right")
        self.assertTrue(ret[1]["eua"] == "both")
        self.assertTrue(ret[1]["cerumen"] == "none")
        self.assertTrue(ret[1]["scarrevision"] == True)
        self.assertTrue(ret[1]["tplastycomment"] == "a tplasty comment")

        x = DeleteENTSurgicalHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTSurgicalHistories(self):
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

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTSurgicalHistory(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setGranuloma("left")
        x.setGranulomaComment("granuloma")
        x.setTubes("left")
        x.setTubesComment("tubes")
        x.setTplasty("right")
        x.setTplastyComment("tplasty")
        x.setEua("both")
        x.setEuaComment("eua")
        x.setFb("none")
        x.setFbComment("fb")
        x.setMyringotomy("left")
        x.setMyringotomyComment("myring")
        x.setCerumen("right")
        x.setCerumenComment("cerumen")
        x.setSeptorhinoplasty(True)
        x.setSeptorhinoplastyComment("septo")
        x.setScarrevision(False)
        x.setScarrevisionComment("scar")
        x.setFrenulectomy(True)
        x.setFrenulectomyComment("fren")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTSurgicalHistory(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTSurgicalHistory(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTSurgicalHistory(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTSurgicalHistory(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTSurgicalHistory(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTSurgicalHistory(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTSurgicalHistory(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTSurgicalHistory(host, port, token)
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
    print("entsurgicalhistory [-h host] [-p port] [-u username] [-w password]") 

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
