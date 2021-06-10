#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
1
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

# -*- coding: utf-8 -*-

'''
Unit tests for covidvac application. Assumes django server is up
and running on the specified host and port
'''
import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreateCOVIDVac(ServiceAPI):
    def __init__(self, host, port, token, payload={}):
        super(CreateCOVIDVac, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = payload

        self.setPayload(self._payload)
        self.setURL("tscharts/v1/covidvac/")

    def setName(self,val):
        self._payload["name"] = val
        self.setPayload(self._payload)

class GetCOVIDVac(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/covidvac/{}/".format(self._id)
        else:
            base = "tscharts/v1/covidvac/"
    
        if not self._name == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "name={}".format(self._name)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetCOVIDVac, self).__init__()
      
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._name = None
        self._id = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()
    
    def setName(self,val):
        self._name = val
        self.makeURL()

class DeleteCOVIDVac(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteCOVIDVac, self).__init__()
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/covidvac/{}/".format(id))

class TestTSCOVIDVac(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]
    
    def testCreateCOVIDVac(self):
        data = {}

        data["name"] = "D0419"

        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
 
        id = int(ret[1]["id"])
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['name'], "D0419")

        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request test uniqueness

        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) # not found        
        
        x = CreateCOVIDVac(host, port, token)
        x.setName("D8765")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        id = int(ret[1]["id"])
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['name'], "D8765")

        x = CreateCOVIDVac(host, port, token)
        x.setName("D8765")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request test uniqueness

        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) # not found        
        
        data = {}
        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data["name"] = "AAAAA"
        data["names"] = "AAAAA"
        data["desc"] = 123 # not a string
        data["category"] = 123 # not a string

        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data = {}
        data["name"] = 123 # not a string
        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
     
    def testDeleteCOVIDVac(self):
        data = {}
        data["name"] = "D9999"

        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        ret = ret[1]
        self.assertEqual(ret["name"], "D9999")
        self.assertEqual(ret["id"], id)

        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) # not found

    def testGetCOVIDVac(self):
        data = {}
        data["name"] = "D1553"
         
        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])

        x = GetCOVIDVac(host, port, token); #test get a cdt by its id
        x.setId(int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        id = int(ret["id"])
        self.assertTrue(ret["name"] == "D1553")
        
        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
       
        x = GetCOVIDVac(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        data = {}
        data["name"] = "D1553"

        x = CreateCOVIDVac(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = ret[1]["id"]

        x = GetCOVIDVac(host, port, token) #test get a cdt by its name
        x.setName("D1553")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue(ret[1][0]["name"] == "D1553")
        self.assertTrue(ret[1][0]["id"] == id)

        x = GetCOVIDVac(host, port, token)
        x.setName("aaaa")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)  #not found      

        x = GetCOVIDVac(host, port, token)
        x.setName("yabba dabba doo")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)  #not found      

        x = DeleteCOVIDVac(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
           
        namelist = ['CCCCC','AAAAA','BBBBB']
        copynamelist = ['CCCCC','AAAAA','BBBBB']
        idlist = []    
        for i in range(0, len(namelist)):
            data = {}
            data["name"] = namelist[i] 
            x = CreateCOVIDVac(host, port, token, data)
            ret = x.send(timeout = 30)
            idlist.append(ret[1]["id"])
            self.assertEqual(ret[0], 200)
        
        x = GetCOVIDVac(host, port, token)   #test get a list of covidvac
        ret = x.send(timeout = 30)    
        for name in namelist:
            for x in ret[1]:
                if name == x["name"]:
                    copynamelist.remove(name)
                    break

        self.assertEqual(copynamelist, [])
 
        for id in idlist:    
            x = DeleteCOVIDVac(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for id in idlist:
            x = GetCOVIDVac(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)  #not found

def usage():
    print("covidvac [-h host] [-p port] [-u username] [-w password]") 

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
