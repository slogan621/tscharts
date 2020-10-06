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
Unit tests for medications application. Assumes django server is up
and running on the specified host and port
'''
import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreateMedications(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreateMedications, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/medications/")

class GetMedications(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/medications/{}/".format(self._id)
        else:
            base = "tscharts/v1/medications/"
    
        if not self._name == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "name={}".format(self._name)
            hasQArgs = True
        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetMedications, self).__init__()
      
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

class DeleteMedications(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteMedications, self).__init__()
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/medications/{}/".format(id))

class TestTSMedications(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]
    
    def testCreateMedications(self):
        data = {}

        data["name"] = "AAAAA"

        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
   
 
        id = int(ret[1]["id"])
        x = GetMedications(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['name'], "AAAAA")

        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request test uniqueness

        x = DeleteMedications(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = GetMedications(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) # not found        
        
        data = {}
        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data["names"] = "AAAAA"

        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data = {}
        data["name"] = ""
        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) 
        
        data = {}
        data["name"] = 123
        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
     
    def testDeleteMedications(self):
        data = {}
        data["name"] = "AAAAA"

        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetMedications(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        ret = ret[1]
        self.assertEqual(ret["name"], "AAAAA")
        self.assertEqual(ret["id"], id)

        x = DeleteMedications(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetMedications(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteMedications(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) # not found

    def testGetMedications(self):
        data = {}
        data["name"] = "AAAAA"
         
        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])

        x = GetMedications(host, port, token); #test get a medication by its id
        x.setId(int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        id = int(ret["id"])
        self.assertTrue(ret["name"] == "AAAAA")
        
        x = DeleteMedications(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
       
        x = GetMedications(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        data = {}
        data["name"] = "CCCCCC"

        x = CreateMedications(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = ret[1]["id"]

        x = GetMedications(host, port, token) #test get a medication by its name
        x.setName("CCCCCC")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue(ret[1]["name"] == "CCCCCC")
        
        x = GetMedications(host, port, token)
        x.setName("aaaa")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)  #not found      

        x = DeleteMedications(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
           
        namelist = ['CCCCC','AAAAA','BBBBB']
        copynamelist = ['CCCCC','AAAAA','BBBBB']
        idlist = []    
        for x in namelist:
            data = {}
            data["name"] = x
            x = CreateMedications(host, port, token, data)
            ret = x.send(timeout = 30)
            idlist.append(ret[1]["id"])
            self.assertEqual(ret[0], 200)
        
        x = GetMedications(host, port, token)   #test get a list of medications
        ret = x.send(timeout = 30)    
        for name in namelist:
            self.assertTrue(name in ret[1])
            copynamelist.remove(name)
        self.assertEqual(copynamelist, [])
 
        for id in idlist:    
            x = DeleteMedications(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for id in idlist:
            x = GetMedications(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)  #not found

def usage():
    print("medications [-h host] [-p port] [-u username] [-w password]") 

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
