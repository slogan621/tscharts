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
unit tests for ent treatment application. Assumes django server is up
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

class ENTTreatmentGenerator():

    sideFields = [
        "earCleanedSide",
        "audiogramSide",
  	"tympanogramSide",
  	"mastoidDebridedSide",
  	"boricAcidSide",
  	"foreignBodyRemoved",
  	"tubesTomorrow",
  	"tPlastyTomorrow",
  	"euaTomorrow",
  	"fbRemovalTomorrow",
  	"middleEarExploreMyringotomyTomorrow",
  	"cerumenTomorrow",
  	"granulomaTomorrow",
  	"tubesFuture",
  	"tPlastyFuture",
  	"euaFuture",
  	"fbRemovalFuture",
  	"middleEarExploreMyringotomyFuture",
  	"cerumenFuture",
  	"granulomaFuture"]

    booleanFields = [
  	"audiogramRightAway",
  	"tympanogramRightAway",
  	"mastoidDebridedHearingAidEval",
  	"antibioticDrops",
  	"antibioticOrally",
  	"antibioticAcuteInfection",
  	"antibioticAfterWaterExposureInfectionPrevention",
  	"boricAcidToday",
  	"boricAcidForHomeUse",
  	"return3Months",
  	"return6Months",
  	"returnPrn",
  	"referredPvtENTEnsenada",
  	"referredChildrensHospitalTJ",
  	"septorhinoplastyTomorrow",
  	"scarRevisionCleftLipTomorrow",
  	"frenulectomyTomorrow",
  	"septorhinoplastyFuture",
  	"scarRevisionCleftLipFuture",
  	"frenulectomyFuture"]

    textFields = [
        "username",
        "earCleanedComment",
  	"audiogramComment",
  	"tympanogramComment",
  	"tympanogramRightAwayComment",
  	"mastoidDebridedComment",
  	"mastoidDebridedHearingAidEvalComment",
  	"antibioticDropsComment",
  	"antibioticOrallyComment",
  	"antibioticAcuteInfectionComment",
  	"antibioticAfterWaterExposureInfectionPreventionComment",
  	"boricAcidTodayComment",
  	"boricAcidForHomeUseComment",
  	"boricAcidSideComment",
  	"foreignBodyRemovedComment",
  	"returnComment",
  	"referredPvtENTEnsenadaComment",
  	"referredChildrensHospitalTJComment",
  	"tubesTomorrowComment",
  	"tPlastyTomorrowComment",
  	"euaTomorrowComment",
  	"fbRemovalTomorrowComment",
  	"middleEarExploreMyringotomyTomorrowComment",
  	"cerumenTomorrowComment",
  	"granulomaTomorrowComment",
  	"septorhinoplastyTomorrowComment",
  	"scarRevisionCleftLipTomorrowComment",
  	"frenulectomyTomorrowComment",
  	"tubesFutureComment",
  	"tPlastyFutureComment",
  	"euaFutureComment",
  	"fbRemovalFutureComment",
  	"middleEarExploreMyringotomyFutureComment",
  	"cerumenFutureComment",
  	"granulomaFutureComment",
  	"septorhinoplastyFutureComment",
  	"scarRevisionCleftLipFutureComment",
  	"frenulectomyFutureComment",
  	"comment"]

    booleanStrings = ["true", "false"]
    sideStrings = ["none", "left", "right", "both"]

    junkKeys = ["jadda", "fooboo", "yeehad"]

    junkSideStrings = ["Both", "LEft", "RIGHT", "noNe", "", None]
    junkBooleanStrings = ["True", "trUe", "FAlse", "faLSE", "", None]
    junkTextStrings = [2654, None, 3.141592654]

    def getRandomJunkKey(self):
        i = random.randrange(len(self.junkKeys))
        return self.junkKeys[i]

    def getRandomJunkBoolean(self):
        i = random.randrange(len(self.junkBooleanStrings))
        return self.junkBooleanStrings[i]

    def getRandomJunkText(self, size):
        i = random.randrange(len(self.junkTextStrings))
        return self.junkTextStrings[i]

    def getRandomJunkSide(self):
        i = random.randrange(len(self.junkSideStrings))
        return self.junkSideStrings[i]

    def getRandomBoolean(self):
        i = random.randrange(len(self.booleanStrings))
        return self.booleanStrings[i]

    def getRandomText(self, size):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])

    def getRandomSide(self):
        i = random.randrange(len(self.sideStrings))
        return self.sideStrings[i]

    def createPayloadBody(self, full):  # full True if POST, False for random PUT
        payload = {}
        for x in self.sideFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomSide()

        for x in self.booleanFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomBoolean()

        count = 0     # len 0, 1, 2, 3, ...
        for x in self.textFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomText(count)
                count += 1

        return payload

    def createJunkPayloadBody(self, full, junkKeys):  
        payload = {}

        if junkKeys:
            for x in range(0, 100):
                payload[self.getRandomText(10)] = self.getRandomJunkSide() 
            for x in range(0, 100):
                payload[self.getRandomText(10)] = self.getRandomJunkBoolean() 
        else:
            for x in self.sideFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkSide()

            for x in self.booleanFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkBoolean()

            count = 0     # len 0, 1, 2, 3, ...
            for x in self.textFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkText(count)
                    count += 1
        return payload

class CreateENTTreatment(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTTreatment, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enttreatment/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)

    def createPayloadBody(self):
        generator = ENTTreatmentGenerator()
        body = generator.createPayloadBody(True) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = ENTTreatmentGenerator()
        body = generator.createJunkPayloadBody(True, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class GetENTTreatment(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/enttreatment/{}/".format(self._id)
        else:
            base = "tscharts/v1/enttreatment/"

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
        super(GetENTTreatment, self).__init__()
        
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

class UpdateENTTreatment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTTreatment, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enttreatment/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def createPayloadBody(self):
        generator = ENTTreatmentGenerator()
        body = generator.createPayloadBody(False) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = ENTTreatmentGenerator()
        body = generator.createJunkPayloadBody(False, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class DeleteENTTreatment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTTreatment, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/enttreatment/{}/".format(id))

class TestTSENTTreatment(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTTreatment(self):
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

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTTreatment(host, port, token)
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

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTTreatment(host, port, token)
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
        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
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

    def testDeleteENTTreatment(self):
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

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200) 

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTTreatment(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTTreatment(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTTreatment(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTTreatment(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTTreatment(self):
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

        x = CreateENTTreatment(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTTreatment(host, port, token, id)
        body = x.createPayloadBody()

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
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
            x = UpdateENTTreatment(host, port, token, id)
            body = x.createPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetENTTreatment(host, port, token)
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
            x = UpdateENTTreatment(host, port, token, id)
            body = x.createJunkPayloadBody(True)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateENTTreatment(host, port, token, id)
            body = x.createJunkPayloadBody(False)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateENTTreatment(host, port, token, id)
            body = x.createPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetENTTreatment(host, port, token)
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

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTTreatments(self):
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

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTTreatment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
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
    print("enttreatment [-h host] [-p port] [-u username] [-w password]") 

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
