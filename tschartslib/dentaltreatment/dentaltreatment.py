#(C) Copyright Syd Logan 2020
#(C) Copyright Thousand Smiles Foundation 2020
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
unit tests for dental treatment application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
import random
import string

class DentalTreatmentSetter(object):

    def __init__(self):
        super(DentalTreatmentSetter, self).__init__()

        self.setters = {
            "localAnestheticBenzocaine": self.setLocalAnestheticBenzocaine,
            "localAnestheticLidocaine": self.setLocalAnestheticLidocaine,
            "localAnestheticSeptocaine": self.setLocalAnestheticSeptocaine,
            "localAnestheticOther": self.setLocalAnestheticOther,
            "localAnestheticNumberCarps": self.setLocalAnestheticNumberCarps,
            "exam": self.setExam,
            "prophy": self.setProphy,
            "srpUR": self.setSrpUR,
            "srpLR": self.setSrpLR,
            "srpUL": self.setSrpUL,
            "srpLL": self.setSrpLL,
            "xraysViewed": self.setXraysViewed,
            "headNeckOralCancerExam": self.setHeadNeckOralCancerExam,
            "oralHygieneInstruction": self.setOralHygieneInstruction,
            "flourideTxVarnish": self.setFlourideTxVarnish,
            "nutritionalCounseling": self.setNutritionalCounseling,
            "orthoEvaluation": self.setOrthoEvaluation,
            "orthoTx": self.setOrthoTx,
            "oralSurgeryEvaluation": self.setOralSurgeryEvaluation,
            "oralSurgeryTx": self.setOralSurgeryTx,
            "username": self.setUsername,
            "examComment": self.setExamComment,
            "prophyComment": self.setProphyComment,
            "srpComment": self.setSrpComment,
            "xraysViewedComment": self.setXraysViewedComment,
            "headNeckOralCancerExamComment": self.setHeadNeckOralCancerExamComment,
            "oralHygieneInstructionComment": self.setOralHygieneInstructionComment,
            "flourideTxVarnishComment": self.setFlourideTxVarnishComment,
            "nutritionalCounselingComment": self.setNutritionalCounselingComment,
            "orthoEvaluationComment": self.setOrthoEvaluationComment,
            "orthoTxComment": self.setOrthoTxComment,
            "oralSurgeryEvaluationComment": self.setOralSurgeryEvaluationComment,
            "oralSurgeryTxComment": self.setOralSurgeryTxComment,
            "localAnestheticComment": self.setLocalAnestheticComment,
            "comment": self.setComment,
        }

    def dispatchSetter(self, key, val):
        try:
            self.setters[key](val)
        except:
            print("dispatchSetter: unable to dispatch {} (val {}) self {} exc {}".format(key, val, self.__dict__, sys.exc_info()[0]))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticBenzocaine(self, val):
        self._payload["localAnestheticBenzocaine"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticLidocaine(self, val):
        self._payload["localAnestheticLidocaine"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticOther(self, val):
        self._payload["localAnestheticOther"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticSeptocaine(self, val):
        self._payload["localAnestheticSeptocaine"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticNumberCarps(self, val):
        self._payload["localAnestheticNumberCarps"] = val
        self.setPayload(self._payload)

    def setExam(self, val):
        self._payload["exam"] = val
        self.setPayload(self._payload)

    def setProphy(self, val):
        self._payload["prophy"] = val
        self.setPayload(self._payload)

    def setSrpUR(self, val):
        self._payload["srpUR"] = val
        self.setPayload(self._payload)

    def setSrpLR(self, val):
        self._payload["srpLR"] = val
        self.setPayload(self._payload)

    def setSrpUL(self, val):
        self._payload["srpUL"] = val
        self.setPayload(self._payload)

    def setSrpLL(self, val):
        self._payload["srpLL"] = val
        self.setPayload(self._payload)

    def setXraysViewed(self, val):
        self._payload["xraysViewed"] = val
        self.setPayload(self._payload)

    def setHeadNeckOralCancerExam(self, val):
        self._payload["headNeckOralCancerExam"] = val
        self.setPayload(self._payload)

    def setOralHygieneInstruction(self, val):
        self._payload["oralHygieneInstruction"] = val
        self.setPayload(self._payload)

    def setFlourideTxVarnish(self, val):
        self._payload["flourideTxVarnish"] = val
        self.setPayload(self._payload)

    def setNutritionalCounseling(self, val):
        self._payload["nutritionalCounseling"] = val
        self.setPayload(self._payload)

    def setOrthoEvaluation(self, val):
        self._payload["orthoEvaluation"] = val
        self.setPayload(self._payload)

    def setOrthoTx(self, val):
        self._payload["orthoTx"] = val
        self.setPayload(self._payload)

    def setOralSurgeryEvaluation(self, val):
        self._payload["oralSurgeryEvaluation"] = val
        self.setPayload(self._payload)

    def setOralSurgeryTx(self, val):
        self._payload["oralSurgeryTx"] = val
        self.setPayload(self._payload)

    def setExamComment(self, val):
        self._payload["examComment"] = val
        self.setPayload(self._payload)

    def setProphyComment(self, val):
        self._payload["prophyComment"] = val
        self.setPayload(self._payload)

    def setSrpComment(self, val):
        self._payload["srpComment"] = val
        self.setPayload(self._payload)

    def setXraysViewedComment(self, val):
        self._payload["xraysViewedComment"] = val
        self.setPayload(self._payload)

    def setHeadNeckOralCancerExamComment(self, val):
        self._payload["headNeckOralCancerExamComment"] = val
        self.setPayload(self._payload)

    def setOralHygieneInstructionComment(self, val):
        self._payload["oralHygieneInstructionComment"] = val
        self.setPayload(self._payload)

    def setFlourideTxVarnishComment(self, val):
        self._payload["flourideTxVarnishComment"] = val
        self.setPayload(self._payload)

    def setNutritionalCounselingComment(self, val):
        self._payload["nutritionalCounselingComment"] = val
        self.setPayload(self._payload)

    def setOrthoEvaluationComment(self, val):
        self._payload["orthoEvaluationComment"] = val
        self.setPayload(self._payload)

    def setOrthoTxComment(self, val):
        self._payload["orthoTxComment"] = val
        self.setPayload(self._payload)

    def setOralSurgeryEvaluationComment(self, val):
        self._payload["oralSurgeryEvaluationComment"] = val
        self.setPayload(self._payload)

    def setOralSurgeryTxComment(self, val):
        self._payload["oralSurgeryTxComment"] = val
        self.setPayload(self._payload)

    def setLocalAnestheticComment(self, val):
        self._payload["localAnestheticComment"] = val
        self.setPayload(self._payload)

    def setComment(self, val):
        self._payload["comment"] = val
        self.setPayload(self._payload)

class DentalTreatmentGenerator():

    integerFields = [
        "localAnestheticNumberCarps",
    ]

    booleanFields = [
        "exam",
        "prophy",
        "srpUR",
        "srpLR",
        "srpUL",
        "srpLL",
        "xraysViewed",
        "headNeckOralCancerExam",
        "oralHygieneInstruction",
        "flourideTxVarnish",
        "nutritionalCounseling",
        "orthoEvaluation",
        "orthoTx",
        "oralSurgeryEvaluation",
        "oralSurgeryTx",
        "localAnestheticBenzocaine",
        "localAnestheticLidocaine",
        "localAnestheticSeptocaine",
        "localAnestheticOther",
    ]

    textFields = [
        "username",
        "examComment",
        "prophyComment",
        "srpComment",
        "xraysViewedComment",
        "headNeckOralCancerExamComment",
        "oralHygieneInstructionComment",
        "flourideTxVarnishComment",
        "nutritionalCounselingComment",
        "orthoEvaluationComment",
        "orthoTxComment",
        "oralSurgeryEvaluationComment",
        "oralSurgeryTxComment",
        "localAnestheticComment",
        "comment",
    ]

    booleanStrings = ["true", "false"]
    anestheticStrings = ["none", "benzocaine", "lidocaine", "septocaine", "other"]

    junkKeys = ["jadda", "fooboo", "yeehad"]

    junkAnestheticStrings = ["Both", "LEft", "RIGHT", "noNe", "", None]
    junkBooleanStrings = ["True", "trUe", "FAlse", "faLSE", "", None]
    junkTextStrings = [2654, 3.141592654]

    def getRandomJunkKey(self):
        i = random.randrange(len(self.junkKeys))
        return self.junkKeys[i]

    def getRandomJunkBoolean(self):
        i = random.randrange(len(self.junkBooleanStrings))
        return self.junkBooleanStrings[i]

    def getRandomJunkText(self, size):
        i = random.randrange(len(self.junkTextStrings))
        return self.junkTextStrings[i]

    def getRandomJunkAnesthetic(self):
        i = random.randrange(len(self.junkAnestheticStrings))
        return self.junkAnestheticStrings[i]

    def getRandomBoolean(self):
        i = random.randrange(len(self.booleanStrings))
        return self.booleanStrings[i]

    def getRandomText(self, size):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])

    def getRandomInteger(self):
        i = random.randint(-999, 999)
        return i

    def createAPIPayloadBody(self, api, full):  # full True if POST, False for random PUT
        payload = {}

        for x in self.integerFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomInteger()
                api.dispatchSetter(x, payload[x])

        for x in self.booleanFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomBoolean()
                api.dispatchSetter(x, payload[x])

        count = 0     # len 0, 1, 2, 3, ...
        for x in self.textFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomText(count)
                api.dispatchSetter(x, payload[x])
                if x == "username" and len(payload[x]) == 0:
                    payload[x] = "username" 
                    api.dispatchSetter(x, payload[x])
                count += 1

        return payload

    def createPayloadBody(self, full):  # full True if POST, False for random PUT
        payload = {}

        for x in self.integerFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomInteger()

        for x in self.booleanFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomBoolean()

        count = 0     # len 0, 1, 2, 3, ...
        for x in self.textFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomText(count)
                if x == "username" and len(payload[x]) == 0:
                    payload[x] = "username" 
                count += 1

        return payload

    def createJunkPayloadBody(self, full, junkKeys):  
        payload = {}

        if junkKeys:
            for x in range(0, 100):
                payload[self.getRandomText(10)] = self.getRandomJunkBoolean() 
        else:
            for x in self.integerFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomInteger()

            for x in self.booleanFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkBoolean()

            count = 0     # len 0, 1, 2, 3, ...
            for x in self.textFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkText(count)
                    count += 1
        return payload

class CreateDentalTreatment(ServiceAPI, DentalTreatmentSetter):
    def __init__(self, host, port, token):
        super(CreateDentalTreatment, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/dentaltreatment/")

    def createAPIPayloadBody(self, x):
        generator = DentalTreatmentGenerator()
        body = generator.createAPIPayloadBody(x, True) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createRandomPayloadBody(self):
        generator = DentalTreatmentGenerator()
        body = generator.createPayloadBody(True) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = DentalTreatmentGenerator()
        body = generator.createJunkPayloadBody(True, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class GetDentalTreatment(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/dentaltreatment/{}/".format(self._id)
        else:
            base = "tscharts/v1/dentaltreatment/"

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
        super(GetDentalTreatment, self).__init__()
        
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
 
    def setClinic(self, val):
        self._clinic = val
        self.makeURL()

    def setPatient(self, val):
        self._patient = val
        self.makeURL()

class UpdateDentalTreatment(ServiceAPI, DentalTreatmentSetter):
    def __init__(self, host, port, token, id):
        super(UpdateDentalTreatment, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/dentaltreatment/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def createRandomPayloadBody(self):
        generator = DentalTreatmentGenerator()
        body = generator.createPayloadBody(False) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = DentalTreatmentGenerator()
        body = generator.createJunkPayloadBody(False, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class DeleteDentalTreatment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteDentalTreatment, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/dentaltreatment/{}/".format(id))

class TestTSDentalTreatment(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateDentalTreatment(self):
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

        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetDentalTreatment(host, port, token)
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

        for x in body:
            self.assertTrue(x in data)
            self.assertTrue(body[x] == data[x])

        x = DeleteDentalTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # no data

        x = CreateDentalTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateDentalTreatment(host, port, token)
        body = x.createJunkPayloadBody(False)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        body = x.createJunkPayloadBody(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
      
        # missing username 
        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setUsername(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testAPICreateDentalTreatment(self):
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

        x = CreateDentalTreatment(host, port, token)
        body = x.createAPIPayloadBody(x)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetDentalTreatment(host, port, token)
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

        for x in body:
            self.assertTrue(x in data)
            self.assertTrue(body[x] == data[x])

        x = DeleteDentalTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateDentalTreatment(host, port, token)
        body = x.createAPIPayloadBody(x)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateDentalTreatment(host, port, token)
        body = x.createAPIPayloadBody(x)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # no data

        x = CreateDentalTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # missing username 
        x = CreateDentalTreatment(host, port, token)
        body = x.createAPIPayloadBody(x)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setUsername(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteDentalTreatment(self):
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

        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200) 

        x = DeleteDentalTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteDentalTreatment(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteDentalTreatment(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteDentalTreatment(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteDentalTreatment(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateDentalTreatment(self):
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

        x = CreateDentalTreatment(host, port, token)
        body = x.createRandomPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateDentalTreatment(host, port, token, id)
        body = x.createRandomPayloadBody()

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        for x in body:
            self.assertTrue(x in ret[1])
            self.assertTrue(body[x] == ret[1][x])

        for i in xrange(0, 500):
            x = UpdateDentalTreatment(host, port, token, id)
            body = x.createRandomPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalTreatment(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertTrue("clinic" in ret[1])
            clinicId = int(ret[1]["clinic"])
            self.assertTrue(clinicId == clinicid)
            self.assertTrue("patient" in ret[1])
            patientId = int(ret[1]["patient"])
            self.assertTrue(patientId == patientid)

            for x in body:
                self.assertTrue(x in ret[1])
                self.assertTrue(body[x] == ret[1][x])

        for i in xrange(0, 500):
            x = UpdateDentalTreatment(host, port, token, id)
            body = x.createJunkPayloadBody(True)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateDentalTreatment(host, port, token, id)
            body = x.createJunkPayloadBody(False)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateDentalTreatment(host, port, token, id)
            body = x.createRandomPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalTreatment(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertTrue("clinic" in ret[1])
            clinicId = int(ret[1]["clinic"])
            self.assertTrue(clinicId == clinicid)
            self.assertTrue("patient" in ret[1])
            patientId = int(ret[1]["patient"])
            self.assertTrue(patientId == patientid)

            for x in body:
                self.assertTrue(x in ret[1])
                self.assertTrue(body[x] == ret[1][x])

        x = DeleteDentalTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllDentalTreatments(self):
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

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalTreatment(host, port, token)
        x.createRandomPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetDentalTreatment(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalTreatment(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalTreatment(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalTreatment(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalTreatment(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalTreatment(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteDentalTreatment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetDentalTreatment(host, port, token)
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
    print("dentaltreatment [-h host] [-p port] [-u username] [-w password]") 

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
