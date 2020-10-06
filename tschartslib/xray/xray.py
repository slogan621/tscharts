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
Unit tests for xray application. Assumes django server is up
and running on the specified host and port
'''
import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateXRay(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateXRay, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/xray/")

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setXRayType(self, val):
        self._payload["xray_type"] = val 
        self.setPayload(self._payload)

    def setMouthType(self, val):
        self._payload["mouth_type"] = val 
        self.setPayload(self._payload)

    def setTeeth(self, val):
        self._payload["teeth"] = val
        self.setPayload(self._payload)

class UpdateXRay(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateXRay, self).__init__()

        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/xray/{}/".format(id))

    def setXRayType(self, val):
        self._payload["xray_type"] = val
        self.setPayload(self._payload)

    def setMouthType(self, val):
        self._payload["mouth_type"] = val
        self.setPayload(self._payload)

    def setTeeth(self, val):
        self._payload["teeth"] = val
        self.setPayload(self._payload)

class GetXRay(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/xray/{}/".format(self._id)
        else:
            base = "tscharts/v1/xray/"
    
        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True
        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True
        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetXRay, self).__init__()
      
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._patient = None
        self._clinic = None
        self._id = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()
    
    def setPatient(self,val):
        self._patient = val
        self.makeURL()

    def setClinic(self,val):
        self._clinic = val
        self.makeURL()

class DeleteXRay(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteXRay, self).__init__()
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/xray/{}/".format(id))

class TestTSXRay(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def createClinics(self, n):
        clinics = []
        for i in range(0, n):
            x = CreateClinic(host, port, token, "Ensenada", "02/05/{}".format(2000 + i), "02/06/{}".format(2000 + i))
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            clinics.append(int(ret[1]["id"]))
        return clinics

    def deleteClinics(self, clinics):
        return
        for i in range(0, len(clinics)):
            x = DeleteClinic(host, port, token, clinics[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
          
    def createPatients(self, n):
        patients = []
        for i in range(0, n):
            data = {}

            data["paternal_last"] = "abcd123{}".format(i)
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
            patients.append(int(ret[1]["id"]))
        return patients

    def deletePatients(self, patients):
        for i in range(0, len(patients)):
            x = DeletePatient(host, port, token, patients[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
          
    def testCreateXRay(self):
        clinics = self.createClinics(2)
        patients = self.createPatients(2)

        x = CreateXRay(host, port, token)
        x.setTeeth(5467)
        x.setXRayType("full")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id1 = int(ret[1]["id"])

        y = GetXRay(host, port, token)
        y.setId(id1)
        ret = y.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['id'], id1)
        self.assertEqual(ret['teeth'], 5467)
        self.assertEqual(ret['xray_type'], "full")
        self.assertEqual(ret['mouth_type'], "adult")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x.setClinic(clinics[1])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200) #ok, different clinic
        id2 = int(ret[1]["id"])

        x.setClinic(clinics[0])
        x.setPatient(patients[1])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200) #ok, different patient
        id3 = int(ret[1]["id"])

        x = DeleteXRay(host, port, token, id1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = DeleteXRay(host, port, token, id2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = DeleteXRay(host, port, token, id3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = CreateXRay(host, port, token)
        x.setTeeth(5467)
        x.setXRayType("anteriors_bitewings")
        x.setMouthType("child")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
 
        id = int(ret[1]["id"])

        y = GetXRay(host, port, token)
        y.setId(id)
        ret = y.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['teeth'], 5467)
        self.assertEqual(ret['xray_type'], "anteriors_bitewings")
        self.assertEqual(ret['mouth_type'], "child")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x = DeleteXRay(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        self.deletePatients(patients)
        self.deleteClinics(clinics)    
     
    def testCreateXRayNegative(self):
        clinics = self.createClinics(1)
        patients = self.createPatients(1)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("nontype")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("")
        x.setMouthType("adult")
        x.setClinic(9999)
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("full")
        x.setMouthType("adult")
        x.setClinic(9999)
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = CreateXRay(host, port, token)
        x.setTeeth(3456)
        x.setXRayType("full")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        self.deletePatients(patients)
        self.deleteClinics(clinics)    
     
    def testDeleteXRay(self):
        clinics = self.createClinics(1)
        patients = self.createPatients(100)
        xrays = []

        for i in range(0,100):
            x = CreateXRay(host, port, token)
            x.setTeeth(5467)
            x.setXRayType("anteriors_bitewings")
            x.setMouthType("adult")
            x.setClinic(clinics[0])
            x.setPatient(patients[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            xrays.append(int(ret[1]["id"]))

        for i in range(0,100):
            x = DeleteXRay(host, port, token, xrays[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

            x = GetXRay(host, port, token)
            x.setId(xrays[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)  # not found

        for i in range(0,len(xrays)):
            x = DeleteXRay(host, port, token, xrays[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)

        self.deletePatients(patients)
        self.deleteClinics(clinics)    

    def testSearchXRay(self):
        clinics = self.createClinics(100)
        patients = self.createPatients(100)
        xrays = []
        types = ("full", "anteriors_bitewings")
        counts = {"full" : 0, "anteriors_bitewings": 0} 
        mouthtypes = ("child", "adult")
        mouthTypeCounts = {"child" : 0, "adult": 0} 

        for i in range(0,100):
            x = CreateXRay(host, port, token)
            x.setTeeth(i)
            if i % 2 == 0:
                x.setXRayType(types[0])
                counts[types[0]] = counts[types[0]] + 1
                x.setMouthType(mouthtypes[0])
                mouthTypeCounts[mouthtypes[0]] = mouthTypeCounts[mouthtypes[0]] + 1
            else:
                x.setXRayType(types[1])
                counts[types[1]] = counts[types[1]] + 1
                x.setMouthType(mouthtypes[1])
                mouthTypeCounts[mouthtypes[1]] = mouthTypeCounts[mouthtypes[1]] + 1

            x.setClinic(clinics[i])
            x.setPatient(patients[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            xrays.append(int(ret[1]["id"]))

        for i in range(0, len(patients)):
            x = GetXRay(host, port, token)
            x.setPatient(patients[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200) 
            t = ret[1];
            self.assertEqual(len(t), 1)
            self.assertEqual(t[0]["patient"], patients[i])

        for i in range(0, len(clinics)):
            x = GetXRay(host, port, token)
            x.setClinic(clinics[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200) 
            t = ret[1];
            self.assertEqual(len(t), 1)
            self.assertEqual(t[0]["clinic"], clinics[i])

        for i in range(0,len(xrays)):
            x = DeleteXRay(host, port, token, xrays[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        self.deletePatients(patients)
        self.deleteClinics(clinics)    

    def testSearchXRayNegative(self):
        clinics = self.createClinics(100)
        patients = self.createPatients(100)
        xrays = []
        types = ("full", "anteriors_bitewings")
        counts = {"full" : 0, "anteriors_bitewings": 0} 
        mouthtypes = ("child", "adult")
        mouthTypeCounts = {"child" : 0, "adult": 0} 

        for i in range(0,100):
            x = CreateXRay(host, port, token)
            x.setTeeth(i)
            if i % 2 == 0:
                x.setXRayType(types[0])
                counts[types[0]] = counts[types[0]] + 1
                x.setMouthType(mouthtypes[0])
                mouthTypeCounts[mouthtypes[0]] = mouthTypeCounts[mouthtypes[0]] + 1
            else:
                x.setXRayType(types[1])
                counts[types[1]] = counts[types[1]] + 1
                x.setMouthType(mouthtypes[1])
                mouthTypeCounts[mouthtypes[1]] = mouthTypeCounts[mouthtypes[1]] + 1

            x.setClinic(clinics[i])
            x.setPatient(patients[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            xrays.append(int(ret[1]["id"]))

        for i in range(0, len(patients)):
            x = GetXRay(host, port, token)
            x.setPatient(patients[i] + 5000)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400)  # missing the clinic, both required

        for i in range(0, len(clinics)):
            x = GetXRay(host, port, token)
            x.setClinic(clinics[i] + 5000)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 400) # missing the patient, both required

        for i in range(0,len(xrays)):
            x = DeleteXRay(host, port, token, xrays[i])
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        self.deletePatients(patients)
        self.deleteClinics(clinics)    

    def testUpdateXRayNegative(self):
        clinics = self.createClinics(1)
        patients = self.createPatients(1)

        x = CreateXRay(host, port, token)
        x.setTeeth(5467)
        x.setXRayType("full")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetXRay(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(int(ret["id"]), id)
        self.assertEqual(ret['teeth'], 5467)
        self.assertEqual(ret['xray_type'], "full")
        self.assertEqual(ret['mouth_type'], "adult")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x = UpdateXRay(host, port, token, 456)
        x.setTeeth(7654)
        x.setXRayType("anteriors_bitewings")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = UpdateXRay(host, port, token, id)
        x.setXRayType("")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = UpdateXRay(host, port, token, id)
        x.setMouthType("")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = UpdateXRay(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = GetXRay(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(int(ret["id"]), id)
        self.assertEqual(ret['teeth'], 5467)
        self.assertEqual(ret['xray_type'], "full")
        self.assertEqual(ret['mouth_type'], "adult")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x = DeleteXRay(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        self.deletePatients(patients)
        self.deleteClinics(clinics)    

    def testUpdateXRay(self):
        clinics = self.createClinics(1)
        patients = self.createPatients(1)

        x = CreateXRay(host, port, token)
        x.setTeeth(5467)
        x.setXRayType("full")
        x.setMouthType("adult")
        x.setClinic(clinics[0])
        x.setPatient(patients[0])
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetXRay(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(int(ret["id"]), id)
        self.assertEqual(ret['teeth'], 5467)
        self.assertEqual(ret['xray_type'], "full")
        self.assertEqual(ret['mouth_type'], "adult")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x = UpdateXRay(host, port, token, id)
        x.setTeeth(7654)
        x.setXRayType("anteriors_bitewings")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetXRay(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(int(ret["id"]), id)
        self.assertEqual(ret['teeth'], 7654)
        self.assertEqual(ret['mouth_type'], "adult")
        self.assertEqual(ret['xray_type'], "anteriors_bitewings")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])

        x = UpdateXRay(host, port, token, id)
        x.setTeeth(1111)
        x.setMouthType("child")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetXRay(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(int(ret["id"]), id)
        self.assertEqual(ret['teeth'], 1111)
        self.assertEqual(ret['xray_type'], "anteriors_bitewings")
        self.assertEqual(ret['clinic'], clinics[0])
        self.assertEqual(ret['patient'], patients[0])
        self.assertEqual(ret['mouth_type'], "child")

        x = DeleteXRay(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        self.deletePatients(patients)
        self.deleteClinics(clinics)

def usage():
    print("xray [-h host] [-p port] [-u username] [-w password]") 

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
