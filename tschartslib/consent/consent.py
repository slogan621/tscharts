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
unit tests for consent application. Assumes django server is up
and running on the specific host and port
'''

import unittest
import getopt, sys
import json
from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.register.register import CreateRegistration, GetRegistration, UpdateRegistration, DeleteRegistration

class CreateConsent(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreateConsent, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/consent/")

class GetConsent(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/consent/{}/".format(self._id)
        else:
            base = "tscharts/v1/consent/"

        if not self._registrationid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "registration={}".format(self._registrationid)
            hasQArgs = True

        if not self._patientid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patientid)
            hasQArgs = True

        if not self._clinicid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinicid)
            hasQArgs = True
        

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetConsent, self).__init__()

        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._id = None
        self._registrationid = None
        self._clinicid = None
        self._patientid = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setRegistration(self, registration):
        self._registrationid = registration
        self.makeURL()

    def setPatient(self, patient):
        self._patientid = patient
        self.makeURL()

    def setClinic(self, clinic):
        self._clinicid = clinic
        self.makeURL()

    

class DeleteConsent(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteConsent, self).__init__()

        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/consent/{}/".format(id))

class testTSConsent(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateConsent(self):
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

        data = {}

        data["paternal_last"] = "1234abcd"
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = True
        data["photo_consent"] = True
        
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        #get consent with consent id
        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],200)        
        self.assertTrue("registration" in ret[1])
        self.assertTrue("patient" in ret[1])
        self.assertTrue("clinic" in ret[1])
                
        registrationId = int(ret[1]["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        
        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == True)
            
        #get consent with registration id
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]
 
        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == True)


        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) #non-exist after delete

        #non-exist registration
        data = {}
        data["registration"] = 9999
        data["clinic"] = clinicid
        data["patient"] = patientid
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        
        #non-exist patient
        data = {}
        data["registration"] = registrationid
        data["clinic"] = clinicid
        data["patient"] = 9999
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        
        #non-exist clinic
        data = {}
        data["registration"] = registrationid
        data["clinic"] = 9999
        data["patient"] = patientid
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        

        #invalid data boolean argu
        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = 123
        data["photo_consent"] = 456
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = "hello"
        data["photo_consent"] = "world"
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        #invalid field name        
        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = True
        data["photo_consent"] = False
        data["hello_world"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        #not contain all the required fields
        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["general_consent"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        #create consent that contains info that doesn't match
        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid1
        data["clinic"] = clinicid
        data["general_consent"] = True
        data["photo_consent"] = False
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        
        #duplicate consent info with same registration
        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = True
        data["photo_consent"] = False
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        id = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid
        data["patient"] = patientid
        data["clinic"] = clinicid
        data["general_consent"] = False
        data["photo_consent"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)


        #delete registration, patient, clinic
        x = DeleteRegistration(host, port, token, registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)


    def testDeleteConsent(self):
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
        registrationid = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid
        data["clinic"] = clinicid
        data["patient"] = patientid
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) #not found

        x = DeleteConsent(host, port, token, 9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteConsent(host, port, token, None)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteConsent(host, port, token, "")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = DeleteConsent(host, port, token, "Hello")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteRegistration(host, port, token, registrationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetConsent(self):
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
        registrationid = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid
        data["clinic"] = clinicid
        data["patient"] = patientid
        data["general_consent"] = True
        data["photo_consent"] = False

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        #get consent with consent id -- a single record returned
        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        
        self.assertTrue("registration" in ret[1])
        self.assertTrue("patient" in ret[1])
        self.assertTrue("clinic" in ret[1])
        
        registrationId = int(ret[1]["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        
        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)


        #get consent with registration id only -- an array containing a single record returned
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        #get consent without consentid and optional params
        x = GetConsent(host, port, token)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0],400)

        #get consent with non-exist consent id
        x = GetConsent(host, port, token)
        x.setId(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #create patient1
        data = {}

        data["paternal_last"] = "1234abcd"
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
        #create patient 2
        data = {}

        data["paternal_last"] = "12abcd"
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
        
        #create patient3
        data = {}

        data["paternal_last"] = "111abcd"
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
        
        #create registration 1
        x = CreateRegistration(host, port, token, patient=patientid1, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid1 = int(ret[1]["id"]) #registrationid1: patientid1 & clinicid

        #create registration 2
        x = CreateRegistration(host, port, token, patient=patientid2, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid2 = int(ret[1]["id"]) #registrationid2: patientid2 & clinicid

        
        
        data = {}
        data["registration"] = registrationid1
        data["clinic"] = clinicid
        data["patient"] = patientid1
        data["general_consent"] = False
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id1 = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid2
        data["clinic"] = clinicid
        data["patient"] = patientid2
        data["general_consent"] = False
        data["photo_consent"] = False

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id2 = int(ret[1]["id"])
        
        #test clinic id only -- an array of items returned
        idlist1 = [id, id1, id2] #The ids correspond with clinicid
        
        x = GetConsent(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        consents = ret[1]
        self.assertTrue(len(consents) == 3)
        for x in consents:
            if x["id"] in idlist1:
                idlist1.remove(x["id"])
        if len(idlist1):
            self.assertTrue("failed to find all created consent items {}".format(idlist1) == None)
        #create clinic 1
        x = CreateClinic(host, port, token, "Ensenada", "02/08/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid1 = int(ret[1]["id"])

        #create clinic 2
        x = CreateClinic(host, port, token, "Ensenada", "02/08/2016", "02/05/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid2 = int(ret[1]["id"])
        
        #create clinic 3
        x = CreateClinic(host, port, token, "Ensenada", "02/08/2016", "02/05/2015")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid3 = int(ret[1]["id"])

        #create registration 3
        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid3 = int(ret[1]["id"]) #registrationid3: patientid & clinicid1

        #create registration 4
        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid4 = int(ret[1]["id"]) #registrationid4: patientid & clinicid2

        #create registration 5
        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid5 = int(ret[1]["id"]) #registrationid5: patientid & clinicid3

        data = {}
        data["registration"] = registrationid3
        data["clinic"] = clinicid1
        data["patient"] = patientid
        data["general_consent"] = False
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id3 = int(ret[1]["id"])

        data = {}
        data["registration"] = registrationid4
        data["clinic"] = clinicid2
        data["patient"] = patientid
        data["general_consent"] = False
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id4 = int(ret[1]["id"])

        idlist2 = [id, id3, id4] #The ids correspond with patientid

        #Get consent with patient id only -- an array of items returned
        x = GetConsent(host, port, token)
        x.setPatient(patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        consents = ret[1]
        self.assertTrue(len(consents) == 3)
        for x in consents:
            if x["id"] in idlist2:
                idlist2.remove(x["id"])
        if len(idlist2):
            self.assertTrue("failed to find all created consent items {}".format(idlist2) == None)

        #Get consent with patient id and clinic id -- an array that contains a single record returned
        x = GetConsent(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        x = GetConsent(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid1)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid1)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == False)
        self.assertTrue(data["photo_consent"] == True)

        #Get consent with patient id and registration id -- an array that contains a single record returns
        
        x = GetConsent(host, port, token)
        x.setPatient(patientid)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        x = GetConsent(host, port, token)
        x.setPatient(patientid1)
        x.setRegistration(registrationid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)

        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid1)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid1)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == False)
        self.assertTrue(data["photo_consent"] == True)

        #get Consent with clinic id and registrion id -- an array that contains a single record returns
       
        x = GetConsent(host, port, token)
        x.setClinic(clinicid)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)

        data = ret[1][0]
        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        x = GetConsent(host, port, token)
        x.setClinic(clinicid)
        x.setRegistration(registrationid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)

        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid1)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid1)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == False)
        self.assertTrue(data["photo_consent"] == True)

        #get consent with registration and patient and clinic ids -- an array that contains a single record returned

        x = GetConsent(host, port, token)
        x.setClinic(clinicid)
        x.setRegistration(registrationid)
        x.setPatient(patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        x = GetConsent(host, port, token)
        x.setClinic(clinicid)
        x.setRegistration(registrationid1)
        x.setPatient(patientid1)
        
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]),1)
        data = ret[1][0]

        self.assertTrue("registration" in data)
        self.assertTrue("patient" in data)
        self.assertTrue("clinic" in data)
        
        registrationId = int(data["registration"])
        self.assertTrue(registrationId == registrationid1)

        clinicId = int(data["clinic"])
        self.assertTrue(clinicId == clinicid)
        
        patientId = int(data["patient"])
        self.assertTrue(patientId == patientid1)
        
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == False)
        self.assertTrue(data["photo_consent"] == True)

        #get consent with patient id that doesn't exist
        x = GetConsent(host, port, token)
        x.setPatient(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #get consent with clinic id that doesn't exist
        x = GetConsent(host, port, token)
        x.setClinic(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #get consent with registration id that doesn't exist
        x = GetConsent(host, port, token)
        x.setRegistration(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #get consent with ids that exist but no record corresponds to it
        x = GetConsent(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        x = GetConsent(host, port, token)
        x.setClinic(clinicid2)
        x.setRegistration(registrationid3)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        x = GetConsent(host, port, token)
        x.setPatient(patientid2)
        x.setRegistration(registrationid3)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        #get consent with patient id that exists but no record corresponds to it
        x = GetConsent(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        #get consent with clinic id that exists but no record corresponds to it
        x = GetConsent(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        #get consent with registration id that exists but no record corresponds to it
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid5)
        ret = x.send(timeout = 30)
        self.assertEqual(200, ret[0])
        self.assertEqual([],ret[1])

        #get consent with registration/patient/clinic id that exists but no record corresponds to it
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid3)
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertEqual([],ret[1])
        
        #delete all the records created
        for x in [id, id1, id2, id3, id4]:
            x = DeleteConsent(host, port, token, x)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in [registrationid, registrationid1, registrationid2, registrationid3, registrationid4, registrationid5]:
            k = DeleteRegistration(host, port, token, x)
            ret = k.send(timeout=30)
            self.assertEqual(ret[0], 200)
       
        for x in [patientid, patientid1, patientid2, patientid3]:
            k = DeletePatient(host, port, token, x)
            ret = k.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in [clinicid, clinicid1, clinicid2, clinicid3]:
            k = DeleteClinic(host, port, token, x)
            ret = k.send(timeout=30)
            self.assertEqual(ret[0], 200)



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
