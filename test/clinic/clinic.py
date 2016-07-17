'''
unit tests for clinic application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

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
    def __init__(self, host, port, token, id):
        super(GetClinic, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinic/{}/".format(id))

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
        x = GetClinic(host, port, token, int(ret[1]["id"]))
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = ret[1]
        self.assertTrue(len(ret) == 1)
        self.assertTrue("id" in ret[0])
        self.assertTrue("location" in ret[0])
        self.assertTrue("start" in ret[0])
        self.assertTrue("end" in ret[0])
        self.assertEqual(ret[0]["location"], "Ensenada")
        self.assertEqual(ret[0]["start"], "02/05/2016")
        self.assertEqual(ret[0]["end"], "02/06/2016")
    
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
        for x in clinics:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to remove items {}".format(ids) == None)

def usage():
    print("tscharts [-h host] [-p port] [-u username] [-w password]") 

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
    port = 80
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
