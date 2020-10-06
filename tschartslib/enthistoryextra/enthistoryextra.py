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
unit tests for ent history extra application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.enthistory.enthistory import CreateENTHistory, DeleteENTHistory
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic

class CreateENTHistoryExtra(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTHistoryExtra, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enthistoryextra/")

    def setENTHistory(self, val):
        self._payload["enthistory"] = val
        self.setPayload(self._payload)
    
    def setName(self, val):
        self._payload["name"] = val 
        self.setPayload(self._payload)
    
    def setDuration(self, val):
        self._payload["duration"] = val 
        self.setPayload(self._payload)
    
    def setSide(self, val):
        self._payload["side"] = val 
        self.setPayload(self._payload)
    
class GetENTHistoryExtra(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/enthistoryextra/{}/".format(self._id)
        else:
            base = "tscharts/v1/enthistoryextra/"

        if not self._enthistory == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "enthistory={}".format(self._enthistory)
            hasQArgs = True

        if not self._name == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "name={}".format(self._name)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetENTHistoryExtra, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._name = None
        self._enthistory = None
        self._id = None
        self.makeURL()

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setName(self, val):
        self._name = val
        self.makeURL()

    def setENTHistory(self, val):
        self._enthistory = val
        self.makeURL()
   
class UpdateENTHistoryExtra(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTHistoryExtra, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enthistoryextra/{}/".format(id))

    def setENTHistory(self, val):
        self._payload[u"enthistory"] = val
        self.setPayload(self._payload)

    def setName(self, val):
        self._payload["name"] = val
        self.setPayload(self._payload)

    def setDuration(self, val):
        self._payload["duration"] = val
        self.setPayload(self._payload)

    def setSide(self, val):
        self._payload["side"] = val
        self.setPayload(self._payload)

class DeleteENTHistoryExtra(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTHistoryExtra, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/enthistoryextra/{}/".format(id))

class TestTSENTHistoryExtra(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTHistoryExtra(self):
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

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")

        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        enthistoryid = int(ret[1]["id"])

        x = CreateENTHistoryExtra(host, port, token)
        x.setENTHistory(enthistoryid)
        x.setName("Somethingitis")
        x.setSide("right")
        x.setDuration("weeks")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["name"], "Somethingitis")  
        self.assertEqual(ret[1]["side"], "right")  

        x = DeleteENTHistoryExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent enthistory

        x = CreateENTHistoryExtra(host, port, token)
        x.setENTHistory(7890)
        x.setName("Somethingelseitis")
        x.setSide("both")
        x.setDuration("intermittent")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistory(host, port, token, enthistoryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteENTHistoryExtra(self):
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

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")

        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        enthistoryid = int(ret[1]["id"])

        x = CreateENTHistoryExtra(host, port, token)
        x.setENTHistory(enthistoryid)
        x.setName("Somethingitis")
        x.setSide("both")
        x.setDuration("intermittent")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTHistoryExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTHistoryExtra(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistoryExtra(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistoryExtra(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTHistoryExtra(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTHistory(host, port, token, enthistoryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTHistoryExtra(self):
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

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")

        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        enthistoryid = int(ret[1]["id"])

        x = CreateENTHistoryExtra(host, port, token)
        x.setENTHistory(enthistoryid)
        x.setName("Somethingitis")
        x.setSide("left")
        x.setDuration("weeks")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("enthistory" in ret[1])
        historyId = int(ret[1]["enthistory"])
        self.assertTrue(enthistoryid == historyId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Somethingitis")
        self.assertTrue(ret[1]["side"] == "left")
        self.assertTrue(ret[1]["duration"] == "weeks")

        x = UpdateENTHistoryExtra(host, port, token, id)
        x.setSide("right")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("enthistory" in ret[1])
        historyId = int(ret[1]["enthistory"])
        self.assertTrue(enthistoryid == historyId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Somethingitis")
        self.assertTrue(ret[1]["side"] == "right")

        x = UpdateENTHistoryExtra(host, port, token, id)
        x.setName("xyz")
        x.setDuration("days")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTHistoryExtra(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("enthistory" in ret[1])
        historyId = int(ret[1]["enthistory"])
        self.assertTrue(enthistoryid == historyId)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "xyz")
        self.assertTrue(ret[1]["side"] == "right")
        self.assertTrue(ret[1]["duration"] == "days")

        x = UpdateENTHistoryExtra(host, port, token, None)
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = UpdateENTHistoryExtra(host, port, token, 6789)
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = UpdateENTHistoryExtra(host, port, token, "")
        x.setName("xyz")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTHistoryExtra(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteENTHistory(host, port, token, enthistoryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTHistoryExtra(self):
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

        x = CreateENTHistory(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setDrainageSide("right")
        x.setDrainageDuration("weeks")
        x.setHearingLossSide("right")
        x.setHearingLossDuration("weeks")
        x.setPainSide("right")
        x.setPainDuration("weeks")

        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        enthistoryid = int(ret[1]["id"])

        delids = []

        for i in range(0, 100):
            x = CreateENTHistoryExtra(host, port, token)
            x.setENTHistory(enthistoryid)
            x.setName("name{}".format(i))
            x.setSide("both")
            x.setDuration("days")

            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            delids.append(ret[1]["id"])

        x = GetENTHistoryExtra(host, port, token)
        x.setENTHistory(enthistoryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 100)

        for x in delids:
            y = DeleteENTHistoryExtra(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteENTHistory(host, port, token, enthistoryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
def usage():
    print("enthistoryextra [-h host] [-p port] [-u username] [-w password]") 

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
