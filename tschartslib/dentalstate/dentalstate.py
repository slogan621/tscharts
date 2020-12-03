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
unit tests for dental state application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.dentalcdt.dentalcdt import CreateDentalCDT, DeleteDentalCDT
import random
import string
import itertools

def breakout(csv):
    #print("breakout csv {}".format(csv))
    ret = []
    x = csv.split(",")
    #print("breakout x {}".format(x))
    for y in x:
        ret.append(y.strip())
    #print("breakout ret {}".format(ret))
    ret.sort() 
    #print("breakout sorted ret {}".format(ret))
    return ret

def permuteAsCSV(strs):
    #print("permuteAsCSV strs {}".format(strs))
    l = list(itertools.permutations(strs))
    #print("permuteAsCSV l {}".format(l))
    csvs = []
    for x in l:
        y = list(x)
        ret = ""
        for z in y:
            if len(ret):
                ret += ","
            ret += z
        csvs.append(ret)
    #print("permuteAsCSV csvs {}".format(csvs))
    return csvs 

def equalSurfaces(a, b):
    return a == b

class DentalStateGenerator():

    integerFields = [
        "tooth",
    ]

    booleanFields = [
    ]

    textFields = [
        "username",
        "comment",
    ]

    stateFields = [
        "state",
    ]

    surfaceFields = [
        "surface",
    ]

    locationFields = [
        "location",
    ]

    booleanStrings = ["true", "false"]
    locationStrings = ["top", "bottom"]
    stateStrings = ["missing", "none", "untreated", "treated", "other"]
    surfaceStrings = ["none", "buccal", "lingual", "mesial", "occlusal", "labial", "incisal", "other"]

    junkKeys = ["jadda", "fooboo", "yeehad"]

    junkStateStrings = ["sdfsdf", "9999", "UnTrEaTeD", "TrEaTeD", "noNe"]
    junkSurfaceStrings = junkStateStrings
    junkLocationStrings = junkStateStrings
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

    def getRandomJunkState(self):
        i = random.randrange(len(self.junkStateStrings))
        return self.junkStateStrings[i]

    def getRandomJunkSurface(self):
        i = random.randrange(len(self.junkSurfaceStrings))
        return self.junkSurfaceStrings[i]

    def getRandomJunkLocation(self):
        i = random.randrange(len(self.junkLocationStrings))
        return self.junkLocationStrings[i]

    def getRandomBoolean(self):
        i = random.randrange(len(self.booleanStrings))
        return self.booleanStrings[i]

    def getRandomText(self, size):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])

    def getRandomState(self):
        i = random.randrange(len(self.stateStrings))
        return self.stateStrings[i]

    def getRandomSurface(self):
        i = random.randrange(len(self.surfaceStrings))
        return self.surfaceStrings[i]

    def getRandomLocation(self):
        i = random.randrange(len(self.locationStrings))
        return self.locationStrings[i]

    def getRandomInteger(self):
        i = random.randint(-999, 999)
        return i

    def createPayloadBody(self, full):  # full True if POST, False for random PUT
        payload = {}

        for x in self.integerFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomInteger()

        for x in self.stateFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomState()

        for x in self.surfaceFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomSurface()

        for x in self.locationFields:
            if full or (not full and self.getRandomBoolean()):
                payload[x] = self.getRandomLocation()

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
                payload[self.getRandomText(10)] = self.getRandomJunkState() 
            for x in range(0, 100):
                payload[self.getRandomText(10)] = self.getRandomJunkSurface() 
            for x in range(0, 100):
                payload[self.getRandomText(10)] = self.getRandomJunkBoolean() 
        else:
            for x in self.integerFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomInteger()

            for x in self.stateFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkState()

            for x in self.booleanFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkBoolean()

            count = 0     # len 0, 1, 2, 3, ...
            for x in self.textFields:
                if full or (not full and self.getRandomBoolean()):
                    payload[x] = self.getRandomJunkText(count)
                    count += 1
        return payload

class CreateDentalState(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateDentalState, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/dentalstate/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)
    
    def setTooth(self, val):
        self._payload["tooth"] = val
        self.setPayload(self._payload)

    def setLocation(self, val):
        self._payload["location"] = val
        self.setPayload(self._payload)
    
    def setCode(self, val):
        self._payload["code"] = val
        self.setPayload(self._payload)
    
    def setState(self, val):
        self._payload["state"] = val
        self.setPayload(self._payload)
    
    def setSurface(self, val):
        self._payload["surface"] = val
        self.setPayload(self._payload)
    
    def setComment(self, val):
        self._payload["comment"] = val
        self.setPayload(self._payload)
    
    def createPayloadBody(self):
        generator = DentalStateGenerator()
        body = generator.createPayloadBody(True) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = DentalStateGenerator()
        body = generator.createJunkPayloadBody(True, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class GetDentalState(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/dentalstate/{}/".format(self._id)
        else:
            base = "tscharts/v1/dentalstate/"

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

        if not self._username == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "username={}".format(self._username)
            hasQArgs = True

        if not self._tooth == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "tooth={}".format(self._tooth)
            hasQArgs = True

        if not self._location == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "location={}".format(self._location)
            hasQArgs = True

        if not self._code == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "code={}".format(self._code)
            hasQArgs = True

        if not self._state == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "state={}".format(self._state)
            hasQArgs = True

        if not self._surface == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "surface={}".format(self._surface)
            hasQArgs = True

        if not self._comment == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "comment={}".format(self._comment)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetDentalState, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._patient = None
        self._username = None
        self._location = None
        self._tooth = None
        self._code = None
        self._state = None
        self._surface = None
        self._comment = None
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

    def setUsername(self, val):
        self._username = val
        self.makeURL()

    def setTooth(self, val):
        self._tooth = val
        self.makeURL()

    def setLocation(self, val):
        self._location = val
        self.makeURL()

    def setCode(self, val):
        self._code = val
        self.makeURL()

    def setState(self, val):
        self._state = val
        self.makeURL()

    def setSurface(self, val):
        self._surface = val
        self.makeURL()

    def setComment(self, val):
        self._comment = val
        self.makeURL()

class UpdateDentalState(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateDentalState, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/dentalstate/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)

    def setTooth(self, val):
        self._payload["tooth"] = val
        self.setPayload(self._payload)

    def setLocation(self, val):
        self._payload["location"] = val
        self.setPayload(self._payload)

    def setCode(self, val):
        self._payload["code"] = val
        self.setPayload(self._payload)

    def setState(self, val):
        self._payload["state"] = val
        self.setPayload(self._payload)

    def setSurface(self, val):
        self._payload["surface"] = val
        self.setPayload(self._payload)

    def setComment(self, val):
        self._payload["comment"] = val
        self.setPayload(self._payload)

    def createPayloadBody(self):
        generator = DentalStateGenerator()
        body = generator.createPayloadBody(False) 
        self._payload = body
        self.setPayload(self._payload)
        return body

    def createJunkPayloadBody(self, junkKeys):
        generator = DentalStateGenerator()
        body = generator.createJunkPayloadBody(False, junkKeys) 
        self._payload = body
        self.setPayload(self._payload)
        return body

class DeleteDentalState(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteDentalState, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/dentalstate/{}/".format(id))

class TestTSDentalState(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateDentalState(self):
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

        x = CreateDentalCDT(host, port, token)
        x.setCode("D1234")
        x.setCategory("Some category")
        x.setDesc("Some description")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        codeid = int(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)

        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        self.assertTrue("code" in ret[1])
        codeId = int(ret[1]["code"])
        self.assertTrue(codeId == codeid)

        data = ret[1]

        for x in body:
            self.assertTrue(x in data)
            self.assertTrue(body[x] == data[x])

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(9999)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setLocation("top")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(9999)
        x.setCode(codeid)
        x.setLocation("top")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent code param

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setLocation("top")
        x.setCode(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # no data

        x = CreateDentalState(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateDentalState(host, port, token)
        body = x.createJunkPayloadBody(False)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        body = x.createJunkPayloadBody(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
      
        # missing username 

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setUsername(None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # test each setter 

        # tooth

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setTooth(15)
        x.setLocation("top")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["tooth"], 15)

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # code

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["code"], codeid)

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # state

        states = DentalStateGenerator.stateStrings

        for state in states:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setSurface("none")
            x.setState(state)
            x.setLocation("top")
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1]["state"], state)

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # location

        locations = DentalStateGenerator.locationStrings

        for location in locations:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setSurface("none")
            x.setState("none")
            x.setLocation(location)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1]["location"], location)

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # surface

        surfaces = permuteAsCSV(DentalStateGenerator.surfaceStrings)

        for surface in surfaces:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState("none")
            x.setSurface(surface)
            x.setLocation("top")
            sf1 = breakout(surface)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            sf2 = breakout(ret[1]["surface"]) 
            self.assertTrue(equalSurfaces(sf1, sf2))

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # comment

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setComment("a comment here")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["comment"], "a comment here")

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # test each search

        # tooth

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setTooth(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setTooth(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["id"], id)
        self.assertEqual(ret[1][0]["tooth"], 15)

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # code

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setCode(codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["id"], id)
        self.assertEqual(ret[1][0]["code"], codeid)

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # state

        states = ["missing", "none", "treated", "untreated", "other"]
        badstates = ["yabba", "dabba", "doo"] 

        for state in states:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState(state)
            x.setSurface("none")
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setState(state)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1][0]["state"], state)
            self.assertEqual(ret[1][0]["id"], id)

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for state in states:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setSurface("none")
            x.setState(state)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            for badstate in badstates:
                x = GetDentalState(host, port, token)
                x.setState(badstate)
                ret = x.send(timeout=30)
                self.assertEqual(ret[0], 400)  

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # location

        locations = DentalStateGenerator.locationStrings
        badlocations = DentalStateGenerator.junkLocationStrings

        for location in locations:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState("none")
            x.setLocation(location)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setLocation(location)
            ret = x.send(timeout=30)
            #print("ret {}".format(ret))
            #print("len of ret[1] {}".format(len(ret[1])))
            #print("ret[1] {}".format(ret[1]))
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1][0]["location"], location)
            self.assertEqual(ret[1][0]["id"], id)

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for location in locations:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState("none")
            x.setLocation(location)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            for badlocation in badlocations:
                x = GetDentalState(host, port, token)
                x.setLocation(badlocation)
                #print("getting badsurface {}".format(badsurface))
                ret = x.send(timeout=30)
                self.assertEqual(ret[0], 400)  

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # surface

        surfaces = DentalStateGenerator.surfaceStrings
        badsurfaces = DentalStateGenerator.junkSurfaceStrings

        for surface in surfaces:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState("none")
            x.setSurface(surface)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            x = GetDentalState(host, port, token)
            x.setSurface(surface)
            ret = x.send(timeout=30)
            #print("ret {}".format(ret))
            #print("len of ret[1] {}".format(len(ret[1])))
            #print("ret[1] {}".format(ret[1]))
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1][0]["state"], "none")
            self.assertEqual(ret[1][0]["id"], id)

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for surface in surfaces:
            x = CreateDentalState(host, port, token)
            body = x.createPayloadBody()
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setState("none")
            x.setSurface(surface)
            x.setCode(codeid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])

            for badsurface in badsurfaces:
                x = GetDentalState(host, port, token)
                x.setSurface(badsurface)
                #print("getting badsurface {}".format(badsurface))
                ret = x.send(timeout=30)
                self.assertEqual(ret[0], 400)  

            x = DeleteDentalState(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        # comment

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCode(codeid)
        x.setComment("a comment here")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setComment("a comment here")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment("a ")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment("comment")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment("here")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment("com")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment(" ")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1][0]["comment"], "a comment here")
        self.assertEqual(ret[1][0]["id"], id)

        x = GetDentalState(host, port, token)
        x.setComment("fooboo")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  

        # cleanup
       
        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteDentalCDT(host, port, token, codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteDentalState(self):
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

        x = CreateDentalCDT(host, port, token)
        x.setCode("D4321")
        x.setCategory("Another category")
        x.setDesc("Another description")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        codeid = int(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setCode(codeid)
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200) 

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteDentalState(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteDentalState(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteDentalState(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteDentalState(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteDentalCDT(host, port, token, codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateDentalState(self):
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

        x = CreateDentalCDT(host, port, token)
        x.setCode("D6655")
        x.setCategory("Yet another category")
        x.setDesc("Yet another description")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        codeid = int(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        body = x.createPayloadBody()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)

        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        self.assertTrue("code" in ret[1])
        codeId = int(ret[1]["code"])
        self.assertTrue(codeId == codeid)

        x = UpdateDentalState(host, port, token, id)
        body = x.createPayloadBody()

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)

        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        self.assertTrue("code" in ret[1])
        codeId = int(ret[1]["code"])
        self.assertTrue(codeId == codeid)

        for x in body:
            self.assertTrue(x in ret[1])
            self.assertTrue(body[x] == ret[1][x])

        for i in xrange(0, 500):
            x = UpdateDentalState(host, port, token, id)
            body = x.createPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  

            self.assertTrue("clinic" in ret[1])
            clinicId = int(ret[1]["clinic"])
            self.assertTrue(clinicId == clinicid)

            self.assertTrue("patient" in ret[1])
            patientId = int(ret[1]["patient"])
            self.assertTrue(patientId == patientid)

            self.assertTrue("code" in ret[1])
            codeId = int(ret[1]["code"])
            self.assertTrue(codeId == codeid)

            for x in body:
                self.assertTrue(x in ret[1])
                self.assertTrue(body[x] == ret[1][x])

        for i in xrange(0, 500):
            x = UpdateDentalState(host, port, token, id)
            body = x.createJunkPayloadBody(True)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateDentalState(host, port, token, id)
            body = x.createJunkPayloadBody(False)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)

        for i in xrange(0, 500):
            x = UpdateDentalState(host, port, token, id)
            body = x.createPayloadBody()
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  

            self.assertTrue("clinic" in ret[1])
            clinicId = int(ret[1]["clinic"])
            self.assertTrue(clinicId == clinicid)

            self.assertTrue("patient" in ret[1])
            patientId = int(ret[1]["patient"])
            self.assertTrue(patientId == patientid)

            self.assertTrue("code" in ret[1])
            codeId = int(ret[1]["code"])
            self.assertTrue(codeId == codeid)

            for x in body:
                self.assertTrue(x in ret[1])
                self.assertTrue(body[x] == ret[1][x])

        # test each setter 

        # tooth

        x = UpdateDentalState(host, port, token, id)
        x.setTooth(23)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["tooth"], 23)

        # code

        x = CreateDentalCDT(host, port, token)
        x.setCode("D8888")
        x.setCategory("cat")
        x.setDesc("desc")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        newcodeid = int(ret[1]["id"])

        x = UpdateDentalState(host, port, token, id)
        x.setCode(newcodeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["code"], newcodeid)

        # location

        locations = ["top", "bottom"]

        for location in locations:
            x = UpdateDentalState(host, port, token, id)
            x.setLocation(location)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1]["location"], location)

        # state

        states = ["missing", "none", "treated", "untreated", "other"]

        for state in states:
            x = UpdateDentalState(host, port, token, id)
            x.setState(state)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            self.assertEqual(ret[1]["state"], state)

        # surfaces

        surfaces = permuteAsCSV(DentalStateGenerator.surfaceStrings)

        for surface in surfaces:
            x = UpdateDentalState(host, port, token, id)
            x.setSurface(surface)
            sf1 = breakout(surface)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetDentalState(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)  
            sf2 = breakout(ret[1]["surface"])
            self.assertTrue(equalSurfaces(sf1, sf2))

        # comment

        x = UpdateDentalState(host, port, token, id)
        x.setComment("booya")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["comment"], "booya")

        # cleanup

        x = DeleteDentalState(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteDentalCDT(host, port, token, codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteDentalCDT(host, port, token, newcodeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)


    def testGetAllDentalStates(self):
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

        x = CreateDentalCDT(host, port, token)
        x.setCode("D2244")
        x.setCategory("category")
        x.setDesc("description")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        codeid = int(ret[1]["id"])

        delids = []

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setCode(codeid)
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setUsername("Gomez")
        x.setCode(codeid)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setCode(codeid)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setCode(codeid)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateDentalState(host, port, token)
        x.createPayloadBody()
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setUsername("Gomez")
        x.setCode(codeid)

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetDentalState(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalState(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalState(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalState(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalState(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetDentalState(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteDentalState(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetDentalState(host, port, token)
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

        x = DeleteDentalCDT(host, port, token, codeid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("dentalstate [-h host] [-p port] [-u username] [-w password]") 

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
