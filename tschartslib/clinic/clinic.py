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
unit tests for clinic application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreateClinic(ServiceAPI):
    def __init__(self, host, port, token, location, start, end):
        super(CreateClinic, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"location": location, "start": start, "end": end}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinic/")
    
class GetClinic(ServiceAPI):
    def makeURL(self):
        url = None
        if self._id:
            if self._date != None:
                url = "tscharts/v1/clinic/{}/?date={}".format(self._id,self._date)
            else:
                url = "tscharts/v1/clinic/{}/".format(self._id)
        else:
            if self._date != None:
                url = "tscharts/v1/clinic/?date={}".format(self._date)
            else:
                url = "tscharts/v1/clinic/"
        self.setURL(url)

    def __init__(self, host, port, token, id=None):
        super(GetClinic, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload) 
        self._id = id
        self._date = None
        self.makeURL()

    def setDate(self, date):
        self._date = date
        self.makeURL()

class GetAllClinics(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllClinics, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinic/")

class DeleteClinic(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteClinic, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinic/{}/".format(id))

class TestTSClinic(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

    def testDeleteClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        x = DeleteClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

    def testGetClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])
        x = GetClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("id" in ret)
        self.assertTrue("location" in ret)
        self.assertTrue("start" in ret)
        self.assertTrue("end" in ret)
        self.assertEqual(ret["location"], "Ensenada")
        self.assertEqual(ret["start"], "02/05/2016")
        self.assertEqual(ret["end"], "02/06/2016")
        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
    
    def testGetClinicByDate(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])
        x = GetClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("id" in ret)
        self.assertTrue("location" in ret)
        self.assertTrue("start" in ret)
        self.assertTrue("end" in ret)
        self.assertEqual(ret["location"], "Ensenada")
        self.assertEqual(ret["start"], "02/05/2016")
        self.assertEqual(ret["end"], "02/06/2016")
    
        x = GetClinic(host, port, token)
        x.setDate("02/05/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("id" in ret)
        self.assertTrue("location" in ret)
        self.assertTrue("start" in ret)
        self.assertTrue("end" in ret)
        self.assertEqual(ret["location"], "Ensenada")
        self.assertEqual(ret["start"], "02/05/2016")
        self.assertEqual(ret["end"], "02/06/2016")
    
        x = GetClinic(host, port, token)
        x.setDate("02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("id" in ret)
        self.assertTrue("location" in ret)
        self.assertTrue("start" in ret)
        self.assertTrue("end" in ret)
        self.assertEqual(ret["location"], "Ensenada")
        self.assertEqual(ret["start"], "02/05/2016")
        self.assertEqual(ret["end"], "02/06/2016")
    
        x = GetClinic(host, port, token)
        x.setDate("02/30/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetClinic(host, port, token)
        x.setDate("02/20/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetClinic(host, port, token)
        x.setDate("02/30")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # empty date same as get all

        x = GetClinic(host, port, token)
        x.setDate("")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1][0])

        x = GetClinic(host, port, token)
        x.setDate("sdfsfsf")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllClinics(self):
        ids = []
        x = CreateClinic(host, port, token, "test1", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = CreateClinic(host, port, token, "test2", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = CreateClinic(host, port, token, "test3", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = GetAllClinics(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinics = ret[1]
        delids = list(ids)
        for x in clinics:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

        for id in delids:
            x = DeleteClinic(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

def usage():
    print("clinic [-h host] [-p port] [-u username] [-w password]") 

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
