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
unit tests for surgery history application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient, GetPatient
from tschartslib.surgerytype.surgerytype import CreateSurgeryType, DeleteSurgeryType, GetSurgeryType

class CreateSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateSurgeryHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setURL("tscharts/v1/surgeryhistory/")

    def setSurgeryHistory(self, history):
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class GetSurgeryHistory(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/surgeryhistory/{}/".format(self._id)
        else:
            base = "tscharts/v1/surgeryhistory/"

        if not self._patientid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patientid)
            hasQArgs = True

        if not self._surgeryid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "surgery={}".format(self._surgeryid)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetSurgeryHistory, self).__init__()

        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._patientid = None
        self._surgeryid = None
        self._id = None
        self.makeURL()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setPatient(self, patient):
        self._patientid = patient
        self.makeURL()

    def setSurgery(self, surgery):
        self._surgeryid = surgery
        self.makeURL()

class UpdateSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateSurgeryHistory, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload) #patientid is fixed
        self.setURL("tscharts/v1/surgeryhistory/{}/".format(id))

    def setSurgeryHistory(self, history): #history might include: surgeryid, year, month, location, anesthesia problem(T/F), bleeding problem(T/F).
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class DeleteSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteSurgeryHistory, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/surgeryhistory/{}/".format(id))

class TestTSSurgeryHistory(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateSurgeryHistory(self):
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

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)
        
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        
        x.setSurgeryHistory(data)
    
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
 
        data = ret[1]
        self.assertTrue("surgery" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgery"] == surgeryid)
        self.assertTrue(data["surgeryyear"] == 1999)
        self.assertTrue(data["surgerymonth"] == 12)
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)

        x = GetSurgeryHistory(host, port, token)
        x.setPatient(patientid)
        x.setSurgery(surgeryid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("surgery" in ret[1][0])
        self.assertTrue("patient" in ret[1][0])
        patientId = int(ret[1][0]["patient"])
        self.assertTrue(patientId == patientid) 
       
        data = ret[1][0]
        self.assertTrue("surgery" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgery"] == surgeryid)
        self.assertTrue(data["surgeryyear"] == 1999)
        self.assertTrue(data["surgerymonth"] == 12)
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)
        
        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) 
        
        #non-exist patient
        data = {}
        data["patient"] = 9999
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
       
        #non-exist surgery 
        data = {}
        data["patient"] = patientid
        data["surgery"] = 9999
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)
        
        #invalid paramter name 
        data = {}
        data["bc"] = 123
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)       
        
        #no data
        x = CreateSurgeryHistory(host, port, token)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
       
        #invalid data boolean argu
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = 123
        data["bleeding_problems"] = 1234
        
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        #invalid surgeryyear
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1952
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        #invalid surgeryyear
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 2050
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        #invalid surgerymonth
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 2000
        data["surgerymonth"] = 15
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        #invalid surgerymonth
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 2000
        data["surgerymonth"] = 0
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
        
        #invalid surgerylocation
        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 2000
        data["surgerymonth"] = 10
        data["surgerylocation"] = ""
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeleteSurgeryType(host, port, token, surgeryid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
    

    def testDeleteSurgeryHistory(self):
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

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)

        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteSurgeryHistory(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteSurgeryHistory(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteSurgeryHistory(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteSurgeryHistory(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteSurgeryType(host, port, token, surgeryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateSurgeryHistory(self):
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

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)

        data = {}
        data["patient"] = patientid
        data["surgery"] = surgeryid
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("surgery" in ret[1])
        surgeryId = ret[1]["surgery"]
        self.assertTrue(surgeryid == surgeryId) 

        data = {}
        data["surgeryyear"] = 2000
        data["surgerymonth"] = 11
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientid == patientId)

        data = ret[1]
        self.assertTrue("surgery" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgery"] == surgeryid)
        self.assertTrue(data["surgeryyear"] == 2000)
        self.assertTrue(data["surgerymonth"] == 11)
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)
        
        data = {}
        data["surgerylocation"] = "Place2"
        data["anesthesia_problems"] = False
        data["bleeding_problems"] = False

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientid == patientId)

        data = ret[1]
        self.assertTrue("surgery" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgery"] == surgeryid)
        self.assertTrue(data["surgeryyear"] == 2000)
        self.assertTrue(data["surgerymonth"] == 11)
        self.assertTrue(data["surgerylocation"] == "Place2")
        self.assertTrue(data["anesthesia_problems"] == False)
        self.assertTrue(data["bleeding_problems"] == False)

        data = {}
        data["anesthesia_problems"] = "hello"
        
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgery"] = None
        
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgeryyear"] = 1900
      
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgeryyear"] = 2500

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgerymonth"] = 24

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        data = {}
        data["surgery"] = 9999

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        data = {}
        data["abc"] = 1234
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {} #update nothing is fine.
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
       
        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        
        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        
        x = DeleteSurgeryType(host, port, token, surgeryid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

    def testGetAllSurgeryHistories(self):
        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid1 = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery2"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid2 = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery3"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid3 = int(ret[1]["id"])

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

        idlist = []
        data = {}
        data["patient"] = patientid1
        data["surgery"] = surgeryid1
        data["surgeryyear"] = 1998
        data["surgerymonth"] = 11
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patient"] = patientid2
        data["surgery"] = surgeryid1
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place2"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patient"] = patientid3
        data["surgery"] = surgeryid1
        data["surgeryyear"] = 2003
        data["surgerymonth"] = 9
        data["surgerylocation"] = "Place3"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)
        
        data = {}
        data["patient"] = patientid1
        data["surgery"] = surgeryid2
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 10
        data["surgerylocation"] = "Place4"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)
        
        data = {}
        data["patient"] = patientid2
        data["surgery"] = surgeryid2
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 9
        data["surgerylocation"] = "Place5"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)
        
        data = {}
        data["patient"] = patientid3
        data["surgery"] = surgeryid2
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 10
        data["surgerylocation"] = "Place6"
        data["anesthesia_problems"] = False
        data["bleeding_problems"] = False
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)
        
        data = {}
        data["patient"] = patientid1
        data["surgery"] = surgeryid3
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 10
        data["surgerylocation"] = "Place7"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patient"] = patientid2
        data["surgery"] = surgeryid3
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 9
        data["surgerylocation"] = "Place8"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patient"] = patientid3
        data["surgery"] = surgeryid3
        data["surgeryyear"] = 2005
        data["surgerymonth"] = 10
        data["surgerylocation"] = "Place9"
        data["anesthesia_problems"] = False
        data["bleeding_problems"] = False
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        x = GetSurgeryHistory(host, port,token)
        x.setPatient(patientid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)
        
        x = GetSurgeryHistory(host, port,token)
        x.setPatient(patientid2)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)
        
        x = GetSurgeryHistory(host, port,token)
        x.setPatient(patientid3)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetSurgeryHistory(host, port, token)
        x.setSurgery(surgeryid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetSurgeryHistory(host, port, token)
        x.setSurgery(surgeryid2)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetSurgeryHistory(host, port, token)
        x.setSurgery(surgeryid3)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in idlist:
            y = DeleteSurgeryHistory(host, port, token, x)
            ret = y.send(timeout = 30)
            self.assertEqual(ret[0], 200)

        for x in idlist:
            y = GetSurgeryHistory(host, port, token)
            y.setId(x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)

        x = DeletePatient(host, port, token, patientid2)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)

        x = DeletePatient(host, port, token, patientid3)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)

        x = DeleteSurgeryType(host, port, token, surgeryid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)

        x = DeleteSurgeryType(host, port, token, surgeryid2)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)

        x = DeleteSurgeryType(host, port, token, surgeryid3)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)
    
def usage():
    print("surgeryhistory [-h host] [-p port] [-u username] [-w password]") 

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

