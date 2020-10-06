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
unit tests for ent diagnosis extra application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.entdiagnosis.entdiagnosis import CreateENTDiagnosis, DeleteENTDiagnosis

class CreateENTDiagnosisExtra(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTDiagnosisExtra, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entdiagnosisextra/")
    
    def setENTDiagnosis(self, val):
        self._payload[u"entdiagnosis"] = val
        self.setPayload(self._payload)

    def setName(self, val):
        self._payload[u"name"] = val
        self.setPayload(self._payload)

    def setValue(self, val):
        self._payload[u"value"] = val
        self.setPayload(self._payload)

class GetENTDiagnosisExtra(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/entdiagnosisextra/{}/".format(self._id)
        else:
            base = "tscharts/v1/entdiagnosisextra/"

        if not self._entdiagnosis == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "entdiagnosis={}".format(self._entdiagnosis)
            hasQArgs = True

        if not self._name == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "name={}".format(self._name)
            hasQArgs = True

        if not self._value == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "value={}".format(self._value)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetENTDiagnosisExtra, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._entdiagnosis = None
        self._name = None
        self._value = None
        self._id = None
        self.makeURL()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setENTDiagnosis(self, val):
        self._entdiagnosis = val
        self.makeURL()

    def setName(self, val):
        self._name = val
        self.makeURL()

    def setValue(self, val):
        self._value = val
        self.makeURL()

class UpdateENTDiagnosisExtra(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTDiagnosisExtra, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/entdiagnosisextra/{}/".format(id))

    def setENTDiagnosis(self, val):
        self._payload[u"entdiagnosis"] = val
        self.setPayload(self._payload)

    def setName(self, val):
        self._payload[u"name"] = val
        self.setPayload(self._payload)

    def setValue(self, val):
        self._payload[u"value"] = val
        self.setPayload(self._payload)

class DeleteENTDiagnosisExtra(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTDiagnosisExtra, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/entdiagnosisextra/{}/".format(id))

class TestTSENTDiagnosisExtra(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]
        self.maxDiff = None

    def testCreateENTDiagnosisExtra(self):
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
        diagnosisid = int(ret[1]["id"])

        x = CreateENTDiagnosisExtra(host, port, token)
        x.setENTDiagnosis(diagnosisid)
        x.setName("Somethingitis")
        x.setValue("75")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["name"], "Somethingitis")  
        self.assertEqual(ret[1]["value"], "75")  

        x = DeleteENTDiagnosisExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent entdiagnosis

        x = CreateENTDiagnosisExtra(host, port, token)
        x.setENTDiagnosis(7890)
        x.setName("Somethingelseitis")
        x.setValue("Some random text")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosis(host, port, token, diagnosisid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteENTDiagnosisExtra(self):
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
        diagnosisid = int(ret[1]["id"])

        x = CreateENTDiagnosisExtra(host, port, token)
        x.setENTDiagnosis(diagnosisid)
        x.setName("Somethingitis")
        x.setValue("75")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTDiagnosisExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTDiagnosisExtra(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosisExtra(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosisExtra(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTDiagnosisExtra(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTDiagnosis(host, port, token, diagnosisid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTDiagnosisExtra(self):
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
        diagnosisid = int(ret[1]["id"])

        x = CreateENTDiagnosisExtra(host, port, token)
        x.setENTDiagnosis(diagnosisid)
        x.setName("Somethingitis")
        x.setValue("75")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("entdiagnosis" in ret[1])
        diagnosisId = int(ret[1]["entdiagnosis"])
        self.assertTrue(diagnosisid == diagnosisId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Somethingitis")
        self.assertTrue(ret[1]["value"] == "75")

        x = UpdateENTDiagnosisExtra(host, port, token, id)
        x.setValue("right is different than left")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("entdiagnosis" in ret[1])
        diagnosisId = int(ret[1]["entdiagnosis"])
        self.assertTrue(diagnosisid == diagnosisId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Somethingitis")
        self.assertTrue(ret[1]["value"] == "right is different than left")

        x = UpdateENTDiagnosisExtra(host, port, token, id)
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTDiagnosisExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("entdiagnosis" in ret[1])
        diagnosisId = int(ret[1]["entdiagnosis"])
        self.assertTrue(diagnosisid == diagnosisId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "xyz")
        self.assertTrue(ret[1]["value"] == "right is different than left")

        x = UpdateENTDiagnosisExtra(host, port, token, None)
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = UpdateENTDiagnosisExtra(host, port, token, 6789)
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = UpdateENTDiagnosisExtra(host, port, token, "")
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTDiagnosisExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteENTDiagnosis(host, port, token, diagnosisid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTDiagnosisExtra(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

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
        patientid = int(ret[1]["id"])

        x = CreateENTDiagnosis(host, port, token)
        sent = x.generateRandomPayload()
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setUsername("Gomez")
        x.setComment("A comment")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        entdiagnosisid = int(ret[1]["id"])

        delids = []

        for i in range(0, 100):
            x = CreateENTDiagnosisExtra(host, port, token)
            x.setENTDiagnosis(entdiagnosisid)
            x.setName("name{}".format(i))
            x.setValue("value{}".format(i))

            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            delids.append(ret[1]["id"])

        x = GetENTDiagnosisExtra(host, port, token)
        x.setENTDiagnosis(entdiagnosisid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 100)

        for x in delids:
            y = DeleteENTDiagnosisExtra(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteENTDiagnosis(host, port, token, entdiagnosisid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("entdiagnosisextra [-h host] [-p port] [-u username] [-w password]") 

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
