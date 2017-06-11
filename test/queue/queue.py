'''
unit tests for queue application. Assumes django server is up
and running on the specified host and port.

Tests cover queue API.
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.station.station import GetAllStations
from test.clinic.clinic import GetAllClinics

# there are no APIs for create, update, or delete. So, these tests must
# be run with the scheduler operating in concert with the schedulter unit
# test, assume that only one clinic is in the database, and will only perform  
# basic positive testing along with negative testing of request args.

class GetQueue(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetQueue, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/queue/")

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)
    
    def setStation(self, station):
        self._payload["station"] = station
        self.setPayload(self._payload)

    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class TestTSQueue(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        global clinicid
        global stationid
        token = ret[1]["token"]

        # attempt to find a clinic in the database

        x = GetAllClinics(host, port, token)
        ret = x.send(timeout=30)
        if ret[0] == 200 and len(ret[1]) > 0:
            clinicid = ret[1][0]["id"]  # take the first

        # attempt to find a station in the database

        x = GetAllStations(host, port, token)
        ret = x.send(timeout=30)
        if ret[0] == 200 and len(ret[1]) > 0:
            stationid = ret[1][0]["id"]  # take the first

    def testGetQueuesForClinic(self):
        x = GetQueue(host, port, token)
        x.setClinic(clinicid)
        print clinicid
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetQueuesForBadClinic(self):
        x = GetQueue(host, port, token)
        x.setClinic(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

    def testGetQueuesForNoClinic(self):
        x = GetQueue(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

    def testGetQueuesForClinicAndStation(self):
        if stationid:
            x = GetQueue(host, port, token)
            x.setClinic(clinicid)
            x.setStation(stationid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

    def testGetQueuesForClinicAndBadStation(self):
        x = GetQueue(host, port, token)
        x.setClinic(clinicid)
        x.setStation(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

    def testGetQueuesForNoClinicAndNoStation(self):
        x = GetQueue(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)


def usage():
    print("queue [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:c:s:")
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
    global clinicid
    clinicid = None
    global stationid
    stationid = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-c":
            clinicid = int(a)
        elif o == "-s":
            stationid = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
