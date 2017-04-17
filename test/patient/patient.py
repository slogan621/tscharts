'''
unit tests for patient application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

class CreatePatient(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreatePatient, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/patient/")

class UpdatePatient(ServiceAPI):
    def __init__(self, host, port, token, id, payload):
        super(UpdatePatient, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload["id"] = id
        self.setPayload(payload)
        self.setURL("tscharts/v1/patient/")

class GetPatient(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(GetPatient, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/patient/{}/".format(id))

class GetAllPatients(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllPatients, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/patient/")

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
        data["gender"] = "f"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetPatient(host, port, token, id)
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
        data["gender"] = "m"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        id = int(ret[1]["id"])
        x = GetPatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        x = DeletePatient(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetPatient(host, port, token, id)
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
        data["gender"] = "m"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        x = GetPatient(host, port, token, int(ret[1]["id"]))
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

        self.assertTrue(ret["paternal_last"] == "abcd1234")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "m")
    
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
        data["gender"] = "m"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        x = GetPatient(host, port, token, int(ret[1]["id"]))
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

        self.assertTrue(ret["paternal_last"] == "abcd1234")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "m")
   
        data["paternal_last"] = "abcdefg" 
        id = int(ret["id"])
        x = UpdatePatient(host, port, token, id, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetPatient(host, port, token, id)
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

        self.assertTrue(ret["paternal_last"] == "abcdefg")
        self.assertTrue(ret["maternal_last"] == "yyyyyy")
        self.assertTrue(ret["first"] == "zzzzzzz")
        self.assertTrue(ret["middle"] == "")
        self.assertTrue(ret["suffix"] == "Jr.")
        self.assertTrue(ret["prefix"] == "")
        self.assertTrue(ret["dob"] == "04/01/1962")
        self.assertTrue(ret["gender"] == "m")
    
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
        data["gender"] = "m"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        data["paternal_last"] = "test2"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        data["paternal_last"] = "test3"
        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        ids.append(ret[1]["id"])
        x = GetAllPatients(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patients = ret[1]
        for x in patients:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

def usage():
    print("patient [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print str(err) 
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
