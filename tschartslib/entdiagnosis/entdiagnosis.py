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
unit tests for ent diagnosis application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json
import random
import copy

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class ENTDiagnosisBase:

    def getRandomSide(self):
        sides = [u"left", u"right", u"both", u"none"]
        x = random.randint(0, len(sides) - 1)
        return sides[x]

    def getRandomBoolean(self):
        ret = False
        x = random.randint(0, 9)
        if x <= 4:
            ret = True
        return ret

    def generateRandomPayload(self):
        '''
        create a random PUT/POST into _payload, then
        return a deep copy of self for use in later
        verfication using GET
        '''

        # members that consist of a ear side

        val = self.getRandomSide()
        self.sethlConductive(val)
        val = self.getRandomSide()
        self.sethl(val)
        val = self.getRandomSide()
        self.sethlMixed(val)
        val = self.getRandomSide()
        self.sethlSensory(val)
        val = self.getRandomSide()
        self.setexternalCerumenImpaction(val)
        val = self.getRandomSide()
        self.setexternalEarCanalFB(val)
        val = self.getRandomSide()
        self.setexternalMicrotia(val)
        val = self.getRandomSide()
        self.settympanicAtelectasis(val)
        val = self.getRandomSide()
        self.settympanicGranuloma(val)
        val = self.getRandomSide()
        self.settympanicMonomer(val)
        val = self.getRandomSide()
        self.settympanicTube(val)
        val = self.getRandomSide()
        self.settympanicPerf(val)
        val = self.getRandomSide()
        self.setmiddleEarCholesteatoma(val)
        val = self.getRandomSide()
        self.setmiddleEarEustTubeDysTMRetraction(val)
        val = self.getRandomSide()
        self.setmiddleEarOtitisMedia(val)
        val = self.getRandomSide()
        self.setmiddleEarSerousOtitisMedia(val)
        val = self.getRandomSide()
        self.setsyndromeHemifacialMicrosomia(val)
        val = self.getRandomSide()
        self.setsyndromePierreRobin(val)

        # members that consist of a boolean

        val = self.getRandomBoolean()
        self.setoralAnkyloglossia(val)
        val = self.getRandomBoolean()
        self.setoralTonsilEnlarge(val)
        val = self.getRandomBoolean()
        self.setoralCleftLipRepairDeformity(val)
        val = self.getRandomBoolean()
        self.setoralCleftLipUnilateral(val)
        val = self.getRandomBoolean()
        self.setoralCleftLipBilateral(val)
        val = self.getRandomBoolean()
        self.setoralCleftLipUnrepaired(val)
        val = self.getRandomBoolean()
        self.setoralCleftLipRepaired(val)
        val = self.getRandomBoolean()
        self.setoralCleftPalateUnilateral(val)
        val = self.getRandomBoolean()
        self.setoralCleftPalateBilateral(val)
        val = self.getRandomBoolean()
        self.setoralCleftPalateUnrepaired(val)
        val = self.getRandomBoolean()
        self.setoralCleftPalateRepaired(val)
        val = self.getRandomBoolean()
        self.setoralSpeechProblem(val)
        val = self.getRandomBoolean()
        self.setnoseDeviatedSeptum(val)
        val = self.getRandomBoolean()
        self.setnoseTurbinateHypertrophy(val)
        val = self.getRandomBoolean()
        self.setnoseDeformitySecondaryToCleftPalate(val)

        return copy.deepcopy(self._payload)

    # setters and getters

    def setClinic(self, val):
        self._payload[u"clinic"] = val
        self.setPayload(self._payload)

    def getClinic(self):
        return self._payload[u"clinic"]
    
    def setPatient(self, val):
        self._payload[u"patient"] = val
        self.setPayload(self._payload)

    def getPatient(self):
        return self._payload[u"patient"]
    
    def setComment(self, val):
        self._payload[u"comment"] = val 
        self.setPayload(self._payload)
    
    def getComment(self):
        return self._payload[u"comment"]

    def setUsername(self, val):
        self._payload[u"username"] = val 
        self.setPayload(self._payload)
    
    def getUsername(self):
        return self._payload[u"username"]

    def sethlConductive(self, val):
        self._payload[u"hlConductive"] = val 
        self.setPayload(self._payload)

    def gethlConductive(self):
        return self._payload[u"hlConductive"]

    def sethl(self, val):
        self._payload[u"hl"] = val
        self.setPayload(self._payload)

    def gethl(self):
        return self._payload[u"hl"]

    def sethlMixed(self, val):
        self._payload[u"hlMixed"] = val
        self.setPayload(self._payload)

    def gethlMixed(self):
        return self._payload[u"hlMixed"]

    def sethlSensory(self, val):
        self._payload[u"hlSensory"] = val
        self.setPayload(self._payload)

    def gethlSensory(self):
        return self._payload[u"hlSensory"]

    def setexternalCerumenImpaction(self, val):
        self._payload[u"externalCerumenImpaction"] = val
        self.setPayload(self._payload)

    def getexternalCerumenImpaction(self):
        return self._payload[u"externalCerumenImpaction"]

    def setexternalEarCanalFB(self, val):
        self._payload[u"externalEarCanalFB"] = val
        self.setPayload(self._payload)

    def getexternalEarCanalFB(self):
        return self._payload[u"externalEarCanalFB"]

    def setexternalMicrotia(self, val):
        self._payload[u"externalMicrotia"] = val
        self.setPayload(self._payload)

    def getexternalMicrotia(self):
        return self._payload[u"externalMicrotia"]

    def settympanicAtelectasis(self, val):
        self._payload[u"tympanicAtelectasis"] = val
        self.setPayload(self._payload)

    def gettympanicAtelectasis(self):
        return self._payload[u"tympanicAtelectasis"]

    def settympanicGranuloma(self, val):
        self._payload[u"tympanicGranuloma"] = val
        self.setPayload(self._payload)

    def gettympanicGranuloma(self):
        return self._payload[u"tympanicGranuloma"]

    def settympanicMonomer(self, val):
        self._payload[u"tympanicMonomer"] = val
        self.setPayload(self._payload)

    def gettympanicMonomer(self):
        return self._payload[u"tympanicMonomer"]

    def settympanicTube(self, val):
        self._payload[u"tympanicTube"] = val
        self.setPayload(self._payload)

    def gettympanicTube(self):
        return self._payload[u"tympanicTube"] 

    def settympanicPerf(self, val):
        self._payload[u"tympanicPerf"] = val
        self.setPayload(self._payload)

    def gettympanicPerf(self):
        return self._payload[u"tympanicPerf"]

    def setmiddleEarCholesteatoma(self, val):
        self._payload[u"middleEarCholesteatoma"] = val
        self.setPayload(self._payload)

    def getmiddleEarCholesteatoma(self):
        return self._payload[u"middleEarCholesteatoma"]

    def setmiddleEarEustTubeDysTMRetraction(self, val):
        self._payload[u"middleEarEustTubeDysTMRetraction"] = val
        self.setPayload(self._payload)

    def getmiddleEarEustTubeDysTMRetraction(self):
        return self._payload[u"middleEarEustTubeDysTMRetraction"]

    def setmiddleEarOtitisMedia(self, val):
        self._payload[u"middleEarOtitisMedia"] = val
        self.setPayload(self._payload)

    def getmiddleEarOtitisMedia(self):
        return self._payload[u"middleEarOtitisMedia"]

    def setmiddleEarSerousOtitisMedia(self, val):
        self._payload[u"middleEarSerousOtitisMedia"] = val
        self.setPayload(self._payload)

    def getmiddleEarSerousOtitisMedia(self):
        return self._payload[u"middleEarSerousOtitisMedia"]

    def setsyndromeHemifacialMicrosomia(self, val):
        self._payload[u"syndromeHemifacialMicrosomia"] = val
        self.setPayload(self._payload)

    def getsyndromeHemifacialMicrosomia(self):
        return self._payload[u"syndromeHemifacialMicrosomia"]

    def setsyndromePierreRobin(self, val):
        self._payload[u"syndromePierreRobin"] = val
        self.setPayload(self._payload)

    def getsyndromePierreRobin(self):
        return self._payload[u"syndromePierreRobin"]

    def setoralAnkyloglossia(self, val):
        self._payload[u"oralAnkyloglossia"] = val
        self.setPayload(self._payload)

    def getoralAnkyloglossia(self):
        return self._payload[u"oralAnkyloglossia"]

    def setoralTonsilEnlarge(self, val):
        self._payload[u"oralTonsilEnlarge"] = val
        self.setPayload(self._payload)

    def getoralTonsilEnlarge(self):
        return self._payload[u"oralTonsilEnlarge"]

    def setoralCleftLipRepairDeformity(self, val):
        self._payload[u"oralCleftLipRepairDeformity"] = val
        self.setPayload(self._payload)

    def getoralCleftLipRepairDeformity(self):
        return self._payload[u"oralCleftLipRepairDeformity"]

    def setoralCleftLipUnilateral(self, val):
        self._payload[u"oralCleftLipUnilateral"] = val
        self.setPayload(self._payload)

    def getoralCleftLipUnilateral(self):
        return self._payload[u"oralCleftLipUnilateral"]

    def setoralCleftLipBilateral(self, val):
        self._payload[u"oralCleftLipBilateral"] = val
        self.setPayload(self._payload)

    def getoralCleftLipBilateral(self):
        return self._payload[u"oralCleftLipBilateral"]

    def setoralCleftLipUnrepaired(self, val):
        self._payload[u"oralCleftLipUnrepaired"] = val
        self.setPayload(self._payload)

    def getoralCleftLipUnrepaired(self):
        return self._payload[u"oralCleftLipUnrepaired"] 

    def setoralCleftLipRepaired(self, val):
        self._payload[u"oralCleftLipRepaired"] = val
        self.setPayload(self._payload)

    def getoralCleftLipRepaired(self):
        return self._payload[u"oralCleftLipRepaired"]

    def setoralCleftPalateUnilateral(self, val):
        self._payload[u"oralCleftPalateUnilateral"] = val
        self.setPayload(self._payload)

    def getoralCleftPalateUnilateral(self):
        return self._payload[u"oralCleftPalateUnilateral"]

    def setoralCleftPalateBilateral(self, val):
        self._payload[u"oralCleftPalateBilateral"] = val
        self.setPayload(self._payload)

    def getoralCleftPalateBilateral(self):
        return self._payload[u"oralCleftPalateBilateral"] 

    def setoralCleftPalateUnrepaired(self, val):
        self._payload[u"oralCleftPalateUnrepaired"] = val
        self.setPayload(self._payload)

    def getoralCleftPalateUnrepaired(self):
        return self._payload[u"oralCleftPalateUnrepaired"]

    def setoralCleftPalateRepaired(self, val):
        self._payload[u"oralCleftPalateRepaired"] = val
        self.setPayload(self._payload)

    def getoralCleftPalateRepaired(self):
        return self._payload[u"oralCleftPalateRepaired"]

    def setoralSpeechProblem(self, val):
        self._payload[u"oralSpeechProblem"] = val
        self.setPayload(self._payload)

    def getoralSpeechProblem(self):
        return self._payload[u"oralSpeechProblem"]

    def setnoseDeviatedSeptum(self, val):
        self._payload[u"noseDeviatedSeptum"] = val
        self.setPayload(self._payload)

    def getnoseDeviatedSeptum(self):
        return self._payload[u"noseDeviatedSeptum"] 

    def setnoseTurbinateHypertrophy(self, val):
        self._payload[u"noseTurbinateHypertrophy"] = val
        self.setPayload(self._payload)

    def getnoseTurbinateHypertrophy(self):
        return self._payload[u"noseTurbinateHypertrophy"]

    def setnoseDeformitySecondaryToCleftPalate(self, val):
        self._payload[u"noseDeformitySecondaryToCleftPalate"] = val
        self.setPayload(self._payload)

    def getnoseDeformitySecondaryToCleftPalate(self):
        return self._payload[u"noseDeformitySecondaryToCleftPalate"]

class CreateENTDiagnosis(ServiceAPI, ENTDiagnosisBase):
    def __init__(self, host, port, token):
        super(CreateENTDiagnosis, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entdiagnosis/")
    
class GetENTDiagnosis(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/entdiagnosis/{}/".format(self._id)
        else:
            base = "tscharts/v1/entdiagnosis/"

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
        super(GetENTDiagnosis, self).__init__()
        
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

class UpdateENTDiagnosis(ServiceAPI, ENTDiagnosisBase):
    def __init__(self, host, port, token, id):
        super(UpdateENTDiagnosis, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entdiagnosis/{}/".format(id))

class DeleteENTDiagnosis(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTDiagnosis, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/entdiagnosis/{}/".format(id))

class TestTSENTDiagnosis(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]
        self.maxDiff = None

    def testCreateENTDiagnosis(self):
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

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        sent[u"time"] = ret[1]["time"]
        sent[u"id"] = ret[1]["id"]
        sent[u"patient"] = ret[1]["patient"]
        sent[u"clinic"] = ret[1]["clinic"]
        sent[u"comment"] = ret[1]["comment"]
        sent[u"username"] = ret[1]["username"]
        self.assertEqual(ret[1], sent)

        x = DeleteENTDiagnosis(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTDiagnosis(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTDiagnosis(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTDiagnosis(host, port, token)
        x.setClinic("abcd")
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateENTDiagnosis(host, port, token)
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

    def testDeleteENTDiagnosis(self):
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

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTDiagnosis(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTDiagnosis(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosis(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosis(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTDiagnosis(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTDiagnosis(self):
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

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setComment("A comment")
        x.setUsername("Gomez")
        x.setPatient(patientid)
        x.setClinic(clinicid)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.settympanicPerf("right")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setnoseTurbinateHypertrophy(False)
        x.setoralCleftLipRepaired(True)
        x.settympanicMonomer("none")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setmiddleEarSerousOtitisMedia("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setoralCleftPalateBilateral(123)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setmiddleEarEustTubeDysTMRetraction(14)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setnoseDeviatedSeptum(999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setnoseDeviatedSeptum(True)
        x.settympanicGranuloma(513)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.settympanicPerf("right")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["tympanicPerf"] == "right")
        self.assertTrue(ret[1]["comment"] == "A comment")
        self.assertTrue(ret[1]["username"] == "Gomez")

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setexternalCerumenImpaction("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTDiagnosis(host, port, token, id)
        x.setnoseTurbinateHypertrophy(False)
        x.setsyndromeHemifacialMicrosomia("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["tympanicPerf"] == "right")
        self.assertTrue(ret[1]["comment"] == "A comment")
        self.assertTrue(ret[1]["username"] == "Gomez")
        self.assertTrue(ret[1]["externalCerumenImpaction"] == "both")
        self.assertTrue(ret[1]["noseTurbinateHypertrophy"] == False)
        self.assertTrue(ret[1]["syndromeHemifacialMicrosomia"] == "both")

        x = DeleteENTDiagnosis(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTDiagnosis(self):
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

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")
        x.setComment("A comment")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTDiagnosis(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTDiagnosis(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTDiagnosis(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTDiagnosis(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTDiagnosis(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTDiagnosis(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTDiagnosis(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTDiagnosis(host, port, token)
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
    print("entdiagnosis [-h host] [-p port] [-u username] [-w password]") 

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
