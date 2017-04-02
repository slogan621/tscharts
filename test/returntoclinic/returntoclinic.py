'''
unit tests for returntoclinic application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.patient.patient import CreatePatient, DeletePatient
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.station.station import CreateStation, DeleteStation

class CreateReturnToClinic(ServiceAPI):
    def __init__(self, host, port, token, clinic, station, patient, interval):
        super(CreateReturnToClinic, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"patient": patient, "clinic": clinic, "station": station, "interval": interval}
        self.setPayload(payload)
        self.setURL("tscharts/v1/returntoclinic/")
    
class GetReturnToClinic(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetReturnToClinic, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        if id:
            self.setURL("tscharts/v1/returntoclinic/{}".format(id))
        else:
            self.setURL("tscharts/v1/returntoclinic/")
    
    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)

    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setStation(self, station):
        self._payload["station"] = station
        self.setPayload(self._payload)

class UpdateReturnToClinic(ServiceAPI):
    def __init__(self, host, port, token, id, interval):
        super(UpdateReturnToClinic, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        payload = {"interval": interval}
        self.setPayload(payload)
        self.setURL("tscharts/v1/returntoclinic/{}/".format(id))

class DeleteReturnToClinic(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteReturnToClinic, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/returntoclinic/{}/".format(id))

class GetAllReturnToClinics(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllReturnToClinics, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/returntoclinic/")

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)

    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setStation(self, station):
        self._payload["station"] = station
        self.setPayload(self._payload)

class TestTSReturnToClinic(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateReturnToClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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
        patientid = int(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=stationid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 3)

        x = DeleteReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateReturnToClinic(host, port, token, clinic=9999, station=stationid, patient=patientid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateReturnToClinic(host, port, token, clinic=clinicid, station=9999, patient=patientid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateReturnToClinic(host, port, token, clinic=clinicid, station=stationid, patient=9999, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # bogus interval param

        x = CreateReturnToClinic(host, port, token, clinic=clinicid, station=stationid, patient=patientid, interval=None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = CreateReturnToClinic(host, port, token, clinic=clinicid, station=stationid, patient=patientid, interval="hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteReturnToClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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
        patientid = int(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=stationid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 3)

        x = DeleteReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteReturnToClinic(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinic(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinic(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteReturnToClinic(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateReturnToClinic(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

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
        patientid = int(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=stationid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 3)

        x = UpdateReturnToClinic(host, port, token, id, 6)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 6)

        x = UpdateReturnToClinic(host, port, token, id, 3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 3)

        x = UpdateReturnToClinic(host, port, token, id, 12)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("interval" in ret[1])
        self.assertTrue(ret[1]["interval"] == 12)

        x = UpdateReturnToClinic(host, port, token, id, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateReturnToClinic(host, port, token, id, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateReturnToClinic(host, port, token, id, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteReturnToClinic(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllReturnToClinics(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

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
        patientid = int(ret[1]["id"])

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

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=entstationid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=dentalstationid, interval=6)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=orthostationid, interval=9)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=screeningstationid, interval=12)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateReturnToClinic(host, port, token, patient=patientid, clinic=clinicid, station=speechstationid, interval=3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 1)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 1)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 1)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 1)

        x = GetAllReturnToClinics(host, port, token)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 5)

        x = GetAllReturnToClinics(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 5)

        for x in rtcs:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to find all created returntoclinic items {}".format(ids) == None)

        for x in delids:
            y = DeleteReturnToClinic(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetAllReturnToClinics(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setStation(screeningstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = GetAllReturnToClinics(host, port, token)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = DeleteStation(host, port, token, orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, screeningstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("returntoclinic [-h host] [-p port] [-u username] [-w password]") 

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
