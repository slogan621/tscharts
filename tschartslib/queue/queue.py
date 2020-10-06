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
unit tests for queue application. Assumes django server is up
and running on the specified host and port.

Tests cover queue API.
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.station.station import GetAllStations
from tschartslib.clinic.clinic import GetAllClinics

# there are no APIs for create, update, or delete. So, these tests must
# be run with the scheduler operating in concert with the schedulter unit
# test, assume that at least one clinic is in the database, and will only 
# perform basic positive testing along with negative testing of request args.

class GetQueue(ServiceAPI):
    def makeURL(self):
        url = "tscharts/v1/queue/"
        hasArgs = False
        if self._clinic != None:
            if not hasArgs:
                url = url + "?"
            else:
                url = url + "&"
            url = url + "clinic={}".format(self._clinic)
            hasArgs = True
        if self._station != None:
            if not hasArgs:
                url = url + "?"
            else:
                url = url + "&"
            url = url + "station={}".format(self._station)
            hasArgs = True
        if self._clinicstation != None:
            if not hasArgs:
                url = url + "?"
            else:
                url = url + "&"
            url = url + "clinicstation={}".format(self._clinicstation)
            hasArgs = True
        self.setURL(url)

    def __init__(self, host, port, token):
        super(GetQueue, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._station = None
        self._clinicstation = None
        self.makeURL()

    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()
    
    def setStation(self, station):
        self._station = station
        self.makeURL()

    def setClinicStation(self, clinicstation):
        self._clinicstation = clinicstation
        self.makeURL()
    
class DeleteQueueEntry(ServiceAPI):
    def makeURL(self):
        url = "tscharts/v1/queueentry/{}/".format(self._queueentryid)
        self.setURL(url)

    def __init__(self, host, port, token):
        super(DeleteQueueEntry, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._queueentryid = None
        self.makeURL()

    def setQueueEntryId(self, queueentryid):
        self._queueentryid = queueentryid
        self.makeURL()
    
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
    print("queue [-h host] [-p port] [-u username] [-w password] [-c clinic] [-s station] [-z clinicstation]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:c:s:z:")
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
    global clinicid
    clinicid = None
    global stationid
    stationid = None
    global clinicstationid
    clinicstationid = None
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
        elif o == "-z":
            clinicstatonid = a
        else:   
            assert False, "unhandled option"
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
