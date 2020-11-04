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

# -*- coding: utf-8 -*-

'''
Unit tests for dentalcdt application. Assumes django server is up
and running on the specified host and port
'''
import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class CreateDentalCDT(ServiceAPI):
    def __init__(self, host, port, token, payload={}):
        super(CreateDentalCDT, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = payload

        self.setPayload(self._payload)
        self.setURL("tscharts/v1/dentalcdt/")

    def setCategory(self,val):
        self._payload["category"] = val
        self.setPayload(self._payload)

    def setCode(self,val):
        self._payload["code"] = val
        self.setPayload(self._payload)

    def setDesc(self,val):
        self._payload["desc"] = val
        self.setPayload(self._payload)

class GetDentalCDT(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/dentalcdt/{}/".format(self._id)
        else:
            base = "tscharts/v1/dentalcdt/"
    
        if not self._category == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "category={}".format(self._category)
            hasQArgs = True

        if not self._code == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "code={}".format(self._code)
            hasQArgs = True

        if not self._desc == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "desc={}".format(self._desc)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetDentalCDT, self).__init__()
      
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._category = None
        self._code = None
        self._desc = None
        self._id = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()
    
    def setCategory(self,val):
        self._category = val
        self.makeURL()

    def setCode(self,val):
        self._code = val
        self.makeURL()

    def setDesc(self,val):
        self._desc = val
        self.makeURL()

class DeleteDentalCDT(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteDentalCDT, self).__init__()
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/dentalcdt/{}/".format(id))

class TestTSDentalCDT(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]
    
    def testCreateDentalCDT(self):
        data = {}

        data["code"] = "D0419"
        data["category"] = "DIAGNOSTIC SERVICES"
        data["desc"] = "assessment of salivary flow by measurement"

        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
 
        id = int(ret[1]["id"])
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['category'], "DIAGNOSTIC SERVICES")
        self.assertEqual(ret['code'], "D0419")
        self.assertEqual(ret['desc'], "assessment of salivary flow by measurement")

        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request test uniqueness

        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) # not found        
        
        x = CreateDentalCDT(host, port, token)
        x.setCode("D8765")
        x.setCategory("Some Category")
        x.setDesc("Insert Description Here")

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
 
        id = int(ret[1]["id"])
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertEqual(ret['category'], "Some Category")
        self.assertEqual(ret['code'], "D8765")
        self.assertEqual(ret['desc'], "Insert Description Here")

        x = CreateDentalCDT(host, port, token)
        x.setCode("D8765")
        x.setCategory("Some Category")
        x.setDesc("Insert Description Here")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request test uniqueness

        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
          
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) # not found        
        
        data = {}
        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data["names"] = "AAAAA"

        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) #bad request

        data = {}
        data["code"] = "D0419"
        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) # missing desc
        
        data = {}
        data["desc"] = "assessment of salivary flow by measurement"
        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400) # missing code
        
        data = {}
        data["code"] = 123 # not a string
        data["desc"] = 123 # not a string
        data["category"] = 123 # not a string
        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
     
    def testDeleteDentalCDT(self):
        data = {}
        data["category"] = "DIAGNOSTIC SERVICES"
        data["code"] = "D9999"
        data["desc"] = "Some description"

        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  

        ret = ret[1]
        self.assertEqual(ret["category"], "DIAGNOSTIC SERVICES")
        self.assertEqual(ret["code"], "D9999")
        self.assertEqual(ret["desc"], "Some description")
        self.assertEqual(ret["id"], id)

        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) # not found

    def testGetDentalCDT(self):
        data = {}
        data["category"] = "DIAGNOSTIC SERVICES"
        data["code"] = "D1553"
        data["desc"] = "Some description"
         
        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])

        x = GetDentalCDT(host, port, token); #test get a cdt by its id
        x.setId(int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        id = int(ret["id"])
        self.assertTrue(ret["category"] == "DIAGNOSTIC SERVICES")
        self.assertTrue(ret["code"] == "D1553")
        self.assertTrue(ret["desc"] == "Some description")
        
        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
       
        x = GetDentalCDT(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        data = {}
        data["category"] = "DIAGNOSTIC SERVICES"
        data["code"] = "D1553"
        data["desc"] = "re-cement or re-bond unilateral space maintainer - per quadrant"

        x = CreateDentalCDT(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = ret[1]["id"]

        x = GetDentalCDT(host, port, token) #test get a cdt by its code
        x.setCode("D1553")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue(ret[1][0]["category"] == "DIAGNOSTIC SERVICES")
        self.assertTrue(ret[1][0]["code"] == "D1553")
        self.assertTrue(ret[1][0]["desc"] == "re-cement or re-bond unilateral space maintainer - per quadrant")
        self.assertTrue(ret[1][0]["id"] == id)

        x = GetDentalCDT(host, port, token) #test get a cdt by its desc
        x.setDesc("re-cement or re-bond unilateral space maintainer - per quadrant")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue(ret[1][0]["category"] == "DIAGNOSTIC SERVICES")
        self.assertTrue(ret[1][0]["code"] == "D1553")
        self.assertTrue(ret[1][0]["desc"] == "re-cement or re-bond unilateral space maintainer - per quadrant")
        self.assertTrue(ret[1][0]["id"] == id)
        
        x = GetDentalCDT(host, port, token)
        x.setCode("aaaa")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)  #not found      

        x = GetDentalCDT(host, port, token)
        x.setCode("yabba dabba doo")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)  #not found      

        x = DeleteDentalCDT(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
           
        codelist = ['CCCCC','AAAAA','BBBBB']
        copycodelist = ['CCCCC','AAAAA','BBBBB']
        desclist = ['111111','222222','333333']
        copydesclist = ['111111','222222','333333']
        idlist = []    
        for i in range(0, len(codelist)):
            data = {}
            data["code"] = codelist[i] 
            data["desc"] = desclist[i] 
            data["category"] = "DIAGNOSTIC SERVICES" 
            x = CreateDentalCDT(host, port, token, data)
            ret = x.send(timeout = 30)
            idlist.append(ret[1]["id"])
            self.assertEqual(ret[0], 200)
        
        x = GetDentalCDT(host, port, token)   #test get a list of dentalcdt
        ret = x.send(timeout = 30)    
        for code in codelist:
            for x in ret[1]:
                if code == x["code"]:
                    copycodelist.remove(code)
                    break

        for desc in desclist:
            for x in ret[1]:
                if desc == x["desc"]:
                    copydesclist.remove(desc)
                    break

        self.assertEqual(copycodelist, [])
        self.assertEqual(copydesclist, [])
 
        for id in idlist:    
            x = DeleteDentalCDT(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for id in idlist:
            x = GetDentalCDT(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)  #not found

def usage():
    print("dentalcdt [-h host] [-p port] [-u username] [-w password]") 

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
