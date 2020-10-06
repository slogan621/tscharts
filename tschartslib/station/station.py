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
unit tests for station application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreateStation(ServiceAPI):
    def __init__(self, host, port, token, name, level=1):
        super(CreateStation, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"name": name, "level": level}
        self.setPayload(payload)
        self.setURL("tscharts/v1/station/")
    
class GetStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(GetStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/station/{}/".format(id))

class GetAllStations(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllStations, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/station/")

class DeleteStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteStation, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/station/{}/".format(id))

class TestTSStation(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateStation(self):
        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertEqual(ret[1]["name"], "ENT")

    def testDeleteStation(self):
        x = CreateStation(host, port, token, "Speech")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        x = DeleteStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

    def testGetStation(self):
        x = CreateStation(host, port, token, "Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        x = GetStation(host, port, token, int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue("id" in ret)
        self.assertTrue("name" in ret)
        self.assertEqual(ret["name"], "Dental")
    
    def testGetAllStations(self):
        ids = []
        x = CreateStation(host, port, token, "test1")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = CreateStation(host, port, token, "test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = CreateStation(host, port, token, "test3")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = GetAllStations(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stations = ret[1]
        for x in stations:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

def usage():
    print("station [-h host] [-p port] [-u username] [-w password]") 

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
