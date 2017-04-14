'''
unit tests for clinic station application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.station.station import CreateStation, DeleteStation

class CreateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, clinic, station, active=False):
        super(CreateClinicStation, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"clinic": clinic, "station": station, "active": active}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/")
    
class GetClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(GetClinicStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinicstation/{}".format(id))

class UpdateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateClinicStation, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        payload = {}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

    def setActive(self, active):
        self._payload["active"] = active
        self.setPayload(self._payload)

    def setLevel(self, level):
        self._payload["level"] = level
        self.setPayload(self._payload)

class GetAllClinicStations(ServiceAPI):
    def __init__(self, host, port, token, clinicid, active):
        super(GetAllClinicStations, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        payload = {"clinic": clinicid, "active": active}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/")

class DeleteClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteClinicStation, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

class TestTSClinicStation(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        # default active state 

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1][0])
        clinicId = int(ret[1][0]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1][0])
        stationId = int(ret[1][0]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit active state

        x = CreateClinicStation(host, port, token, clinicid, stationid, False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1][0])
        clinicId = int(ret[1][0]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1][0])
        stationId = int(ret[1][0]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1][0])
        clinicId = int(ret[1][0]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1][0])
        stationId = int(ret[1][0]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == True)
        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateClinicStation(host, port, token, 9999, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateClinicStation(host, port, token, clinicid, 9999, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # bogus active state param

        x = CreateClinicStation(host, port, token, clinicid, stationid, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == True) 

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == False)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1][0])
        self.assertTrue(ret[1][0]["active"] == True)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1][0])
        self.assertTrue(int(ret[1][0]["level"]) == 15)
        self.assertTrue(ret[1][0]["active"] == True)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(0)
        x.setActive(False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1][0])
        self.assertTrue(int(ret[1][0]["level"]) == 0)
        self.assertTrue(ret[1][0]["active"] == False)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllClinicStations(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        entstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        dentalstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Ortho")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        orthostationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Screening")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        screeningstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Speech")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        speechstationid = int(ret[1]["id"])

        ids = []
        delids = []
        x = CreateClinicStation(host, port, token, clinicid, entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, screeningstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = GetAllClinicStations(host, port, token, clinicid, False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stations = ret[1]
        self.assertTrue(len(stations) == 5)
        for x in stations:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to find all created clinicstation items {}".format(ids) == None)

        for x in delids:
            y = DeleteClinicStation(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetAllClinicStations(host, port, token, clinicid, False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        stations = ret[1]
        self.assertTrue(len(stations) == 0)

def usage():
    print("clinicstations [-h host] [-p port] [-u username] [-w password]") 

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
