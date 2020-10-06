#(C) Copyright Syd Logan 2016-2020
#(C) Copyright Thousand Smiles Foundation 2016-2020
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
unit tests for patient application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreatePatient(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreatePatient, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        # default CURP is ""

        if not "curp" in payload:
            payload["curp"] = ""

        # same with oldid

        if not "oldid" in payload:
            payload["oldid"] = -1 

        self.setPayload(payload)
        self.setURL("tscharts/v1/patient/")

class UpdatePatient(ServiceAPI):
    def __init__(self, host, port, token, id, payload):
        super(UpdatePatient, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/patient/{}/".format(id))

class GetPatient(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/patient/{}/".format(self._id)
        else:
            base = "tscharts/v1/patient/"
        
        if not self._name == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "name={}".format(self._name)
            hasQArgs = True 
        
        if not self._curp == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "curp={}".format(self._curp)
            hasQArgs = True 
        
        if not self._oldid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "oldid={}".format(self._oldid)
            hasQArgs = True 
        
        if not self._paternalLast == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "paternal_last={}".format(self._paternalLast)
            hasQArgs = True 
        
        if not self._first == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "first={}".format(self._first)
            hasQArgs = True 
        
        if not self._dob == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "dob={}".format(self._dob)
            hasQArgs = True 

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetPatient, self).__init__()
      
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._paternalLast = None
        self._first = None
        self._name = None
        self._dob = None
        self._id = None
        self._curp = None
        self._oldid = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setCurp(self, curp):
        self._curp = curp;
        self.makeURL()

    def setOldid(self, val):
        self._oldid = val;
        self.makeURL()

    def setPaternalLast(self, val):
        self._paternalLast = val
        self.makeURL()

    def setFirstName(self, val):
        self._first = val;
        self.makeURL()

    def setName(self, val):
        self._name = val;
        self.makeURL()

    def setDob(self, val):
        self._dob = val;
        self.makeURL()

class DeletePatient(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeletePatient, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/patient/{}/".format(id))

class TestTSPatient(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreatePatient(self):
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
        data["curp"] = "1234"
        data["oldid"] = 8888

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetPatient(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeletePatient(self):
        data = {}

        data["paternal_last"] = "abcd1234"
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
        data["curp"] = "5678"
        data["oldid"] = 5467

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetPatient(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetPatient(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) # not found

    def testGetPatient(self):

        data = {}
        data["paternal_last"] = "abcd1234"
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
        data["curp"] = "abcd"
        data["oldid"] = 1234

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        x = GetPatient(host, port, token);
        x.setId(int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        id = int(ret["id"])
        self.assertTrue("paternal_last" in ret)
        self.assertTrue("maternal_last" in ret)
        self.assertTrue("first" in ret)
        self.assertTrue("middle" in ret)
        self.assertTrue("suffix" in ret)
        self.assertTrue("prefix" in ret)
        self.assertTrue("dob" in ret)
        self.assertTrue("gender" in ret)
        self.assertTrue("curp" in ret)
        self.assertTrue("oldid" in ret)

        self.assertTrue(ret["paternal_last"] == "abcd1234")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "Male")
        self.assertTrue(ret["curp"] == "abcd")
        self.assertTrue(ret["oldid"] == 1234)
    
        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdatePatient(self):

        data = {}
        data["paternal_last"] = "abcd1234"
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
        data["curp"] = "1234"
        data["oldid"] = 7799

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        x = GetPatient(host, port, token)
        x.setId(int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("paternal_last" in ret)
        self.assertTrue("maternal_last" in ret)
        self.assertTrue("first" in ret)
        self.assertTrue("middle" in ret)
        self.assertTrue("suffix" in ret)
        self.assertTrue("prefix" in ret)
        self.assertTrue("dob" in ret)
        self.assertTrue("gender" in ret)
        self.assertTrue("curp" in ret)
        self.assertTrue("oldid" in ret)

        self.assertTrue(ret["paternal_last"] == "abcd1234")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "Male")
        self.assertTrue(ret["curp"] == "1234")
        self.assertTrue(ret["oldid"] == 7799)
   
        data["paternal_last"] = "abcdefg" 
        id = int(ret["id"])
        x = UpdatePatient(host, port, token, id, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetPatient(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("paternal_last" in ret)
        self.assertTrue("maternal_last" in ret)
        self.assertTrue("first" in ret)
        self.assertTrue("middle" in ret)
        self.assertTrue("suffix" in ret)
        self.assertTrue("prefix" in ret)
        self.assertTrue("dob" in ret)
        self.assertTrue("gender" in ret)
        self.assertTrue("curp" in ret)
        self.assertTrue("oldid" in ret)

        self.assertTrue(ret["paternal_last"] == "abcdefg")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "Male")
        self.assertTrue(ret["curp"] == "1234")
        self.assertTrue(ret["oldid"] == 7799)
    
        data["paternal_last"] = "xxyyzz" 
        data["gender"] = "Female" 
        data["curp"] = "z1u2" 
        data["oldid"] = 1234 
        id = int(ret["id"])
        x = UpdatePatient(host, port, token, id, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetPatient(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("paternal_last" in ret)
        self.assertTrue("maternal_last" in ret)
        self.assertTrue("first" in ret)
        self.assertTrue("middle" in ret)
        self.assertTrue("suffix" in ret)
        self.assertTrue("prefix" in ret)
        self.assertTrue("dob" in ret)
        self.assertTrue("gender" in ret)
        self.assertTrue("curp" in ret)
        self.assertTrue("oldid" in ret)

        self.assertTrue(ret["paternal_last"] == "xxyyzz")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "Female")
        self.assertTrue(ret["curp"] == "z1u2")
        self.assertTrue(ret["oldid"] == 1234)
    
        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testSearchPatient(self):
        ids = []

        data = {}
        data["paternal_last"] = "test1"
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
        data["curp"] = "1111"
        data["oldid"] = 9999

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test1id = ret[1]["id"]

        data["paternal_last"] = "test2"
        data["first"] = "yyyyyyy"
        data["dob"] = "04/01/1962"
        data["curp"] = "2222"
        data["oldid"] = 8888
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test2id = ret[1]["id"]

        data["paternal_last"] = "test3"
        data["first"] = "yyyyyyy"
        data["dob"] = "04/02/1962"
        data["curp"] = "3333"
        data["oldid"] = 7777
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test3id = ret[1]["id"]

        data["paternal_last"] = "test4"
        data["first"] = "xxxxxxx"
        data["dob"] = "04/02/1962"
        data["curp"] = "4444"
        data["oldid"] = 6666
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test4id = ret[1]["id"]

        data["paternal_last"] = "test5"
        data["first"] = "qqqqqqq"
        data["dob"] = "04/03/1962"
        data["curp"] = "5555"
        data["oldid"] = 5555
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test5id = ret[1]["id"]

        data["paternal_last"] = "test6"
        data["first"] = "qqqqqqq"
        data["dob"] = "04/03/1962"
        data["curp"] = "6666"
        data["oldid"] = 4444
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        test6id = ret[1]["id"]

        x = GetPatient(host, port, token)
        x.setPaternalLast("test5")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(ret[0], test5id)

        x = GetPatient(host, port, token)
        x.setCurp("1111")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test1id in ret)

        x = GetPatient(host, port, token)
        x.setCurp("2222")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test2id in ret)

        x = GetPatient(host, port, token)
        x.setCurp("3333")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test3id in ret)

        x = GetPatient(host, port, token)
        x.setCurp("4444")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test4id in ret)

        x = GetPatient(host, port, token)
        x.setCurp("5555")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test5id in ret)

        x = GetPatient(host, port, token)
        x.setCurp("6666")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test6id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("9999")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test1id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("8888")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test2id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("7777")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test3id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("6666")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test4id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("5555")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test5id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("4444")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test6id in ret)

        x = GetPatient(host, port, token)
        x.setOldid("87976")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetPatient(host, port, token)
        x.setDob("04/03/1962")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 2)
        self.assertTrue(test5id in ret)
        self.assertTrue(test6id in ret)

        x = GetPatient(host, port, token)
        x.setDob("04/1962")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetPatient(host, port, token)
        x.setDob("05/1962")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetPatient(host, port, token)
        x.setFirstName("x")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test4id in ret)

        x = GetPatient(host, port, token)
        x.setPaternalLast("st1")
        x.setFirstName("z")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue(test1id in ret)

        x = GetPatient(host, port, token)
        x.setPaternalLast("Flintstone")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetPatient(host, port, token)
        x.setDob("1/1/1970")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetPatient(host, port, token)
        x.setOldid("vvvvvv")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetPatient(host, port, token)
        x.setFirstName("Fred")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetPatient(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        patients = ret[1]
        for x in patients:
            ids.remove(x)
            x = DeletePatient(host, port, token, x)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

    def testGetAllPatients(self):
        ids = []

        data = {}
        data["paternal_last"] = "test1"
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
        data["curp"] = "11-22-33-44"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        data["paternal_last"] = "test2"
        data["curp"] = "22-33-44-55"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        data["paternal_last"] = "test3"
        data["curp"] = "33-44-55-66"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = GetPatient(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patients = ret[1]

        for x in patients:
            ids.remove(x)
            x = DeletePatient(host, port, token, x)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

def usage():
    print("patient [-h host] [-p port] [-u username] [-w password]") 

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
