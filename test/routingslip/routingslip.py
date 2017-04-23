'''
unit tests for routingslip application. Assumes django server is up
and running on the specified host and port.

Tests cover routingslip, routingslipcomment, and routingslipentry URLs.
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.patient.patient import CreatePatient, DeletePatient
from test.station.station import CreateStation, DeleteStation
from test.clinicstation.clinicstation import CreateClinicStation, DeleteClinicStation
from test.clinic.clinic import CreateClinic, DeleteClinic

class CreateRoutingSlip(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateRoutingSlip, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/routingslip/")

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)
    
    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def setCategory(self, category):
        self._payload["category"] = category
        self.setPayload(self._payload)
    
class GetRoutingSlip(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetRoutingSlip, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        if not id:
            self.setURL("tscharts/v1/routingslip/")
        else:
            self.setURL("tscharts/v1/routingslip/{}".format(id))

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)
    
    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)

    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class UpdateRoutingSlip(ServiceAPI):
    def __init__(self, host, port, token, id, category):
        super(UpdateRoutingSlip, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        payload = {"category": category}
        self.setPayload(payload)
        self.setURL("tscharts/v1/routingslip/{}/".format(id))

    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class DeleteRoutingSlip(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteRoutingSlip, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/routingslip/{}/".format(id))

class CreateRoutingSlipEntry(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateRoutingSlipEntry, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/routingslipentry/")

    def setClinicStation(self, clinicstation):
        self._payload["clinicstation"] = clinicstation
        self.setPayload(self._payload)
    
    def setRoutingSlip(self, routingslip):
        self._payload["routingslip"] = routingslip
        self.setPayload(self._payload)

    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class GetRoutingSlipEntry(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetRoutingSlipEntry, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        if not id:
            self.setURL("tscharts/v1/routingslipentry/")
        else:
            self.setURL("tscharts/v1/routingslipentry/{}".format(id))

    def setRoutingslip(self, routingslip):
        self._payload["routingslip"] = routingslip
        self.setPayload(self._payload)
    
    def setClinicStation(self, clinicstation):
        self._payload["clinicstation"] = clinicstation
        self.setPayload(self._payload)
    
class UpdateRoutingSlipEntry(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateRoutingSlipEntry, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/routingslipentry/{}/".format(id))

    def setOrder(self, order):
        self._payload["order"] = order
        self.setPayload(self._payload)

    def setState(self, state):
        self._payload["state"] = state
        self.setPayload(self._payload)
    
    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class DeleteRoutingSlipEntry(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteRoutingSlipEntry, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/routingslipentry/{}/".format(id))

class CreateRoutingSlipComment(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateRoutingSlipComment, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/routingslipcomment/")

    def setRoutingSlip(self, routingslip):
        self._payload["routingslip"] = routingslip
        self.setPayload(self._payload)
    
    def setComment(self, comment):
        self._payload["comment"] = comment
        self.setPayload(self._payload)

    def setAuthor(self, author):
        self._payload["author"] = author
        self.setPayload(self._payload)
    
    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class GetRoutingSlipComment(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetRoutingSlipComment, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        if not id:
            self.setURL("tscharts/v1/routingslipcomment/")
        else:
            self.setURL("tscharts/v1/routingslipcomment/{}".format(id))

    def setRoutingSlip(self, routingslip):
        self._payload["routingslip"] = routingslip
        self.setPayload(self._payload)
    
    def clearPayload(self):
        self._payload = {}
        self.setPayload(self._payload)
    
class DeleteRoutingSlipComment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteRoutingSlipComment, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/routingslipcomment/{}/".format(id))

class TestTSRoutingSlip(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateRoutingSlip(self):
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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = GetRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipid)
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("category" in ret[1]);
        self.assertTrue("routing" in ret[1]);
        self.assertTrue("comments" in ret[1]);
        self.assertTrue(ret[1]["category"] == "New Cleft");
        self.assertTrue(len(ret[1]["routing"]) == 0)
        self.assertTrue(len(ret[1]["comments"]) == 0)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipBadClinic(self):

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        x.setCategory("Returning Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipBadPatient(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        x.setCategory("Returning Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
 
    def testCreateRoutingSlipBadCategory(self):
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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("new york")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
 
        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
 
    def testCreateMultipleRoutingSlip(self):

        patients = []
        routingslips = []

        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        for i in xrange(0, 100):
            data = {}
            data["paternal_last"] = "{}abcd1234".format(i)
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
            patients.append(patientid)

            x = CreateRoutingSlip(host, port, token)
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setCategory("New Cleft")
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            routingslipid = int(ret[1]["id"])
            routingslips.append(routingslipid)

        for i in routingslips:
            x = GetRoutingSlip(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == i)
            self.assertTrue(int(ret[1]["clinic"] == clinicid))
            pid = int(ret[1]["patient"])
            self.assertTrue(pid in patients)
            patients.remove(pid)

        self.assertTrue(len(patients) == 0)

        for i in routingslips:
            x = DeleteRoutingSlip(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteRoutingSlip(self):

        # create routingslip, delete, verify it is gone

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("Other")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = GetRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipid)
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("category" in ret[1]);
        self.assertTrue(ret[1]["category"] == "Other");

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # try deleting an invalid routingslip

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # create a few routingslip objects, delete them
        # and verify there are none in the database

        data = {}
        data["paternal_last"] = "plast1"
        data["maternal_last"] = "mlast1"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "f"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid1 = int(ret[1]["id"])

        data["paternal_last"] = "plast2"
        data["maternal_last"] = "mlast2"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data["paternal_last"] = "plast3"
        data["maternal_last"] = "mlast3"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        ids = []
        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid1)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid2)
        x.setCategory("Unknown")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid3)
        x.setCategory("Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        for x in ids:
            y = GetRoutingSlip(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == x)

        for x in ids:
            y = DeleteRoutingSlip(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in ids:
            y = GetRoutingSlip(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateRoutingSlip(self):

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = GetRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipid)
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("category" in ret[1]);
        self.assertTrue(ret[1]["category"] == "New Cleft");

        x = UpdateRoutingSlip(host, port, token, routingslipid, "Ortho")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipid)
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("category" in ret[1]);
        self.assertTrue(ret[1]["category"] == "Ortho");

        x = UpdateRoutingSlip(host, port, token, routingslipid, "abc")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateRoutingSlip(host, port, token, routingslipid, "123")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateRoutingSlip(host, port, token, routingslipid, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipid)
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        self.assertTrue(int(ret[1]["patient"] == patientid))
        self.assertTrue("category" in ret[1]);
        self.assertTrue(ret[1]["category"] == "Ortho");

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllRoutingSlip(self):

        patients = []
        routingslips = []

        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        for i in xrange(0, 100):
            data = {}
            data["paternal_last"] = "{}abcd1234".format(i)
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
            patients.append(patientid)

            x = CreateRoutingSlip(host, port, token)
            x.setClinic(clinicid)
            x.setPatient(patientid)
            x.setCategory("New Cleft")
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            routingslipid = int(ret[1]["id"])
            routingslips.append(routingslipid)

        # get all routing slips based on search terms

        # search on clinic, returns array

        x = GetRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        results = ret[1]
        self.assertTrue(len(results) == 100)
        for i in results:
            self.assertTrue("id" in i)
            self.assertTrue(i["clinic"] == clinicid)
            pid = int(i["patient"])
            self.assertTrue(pid in patients)

        # search on patient, returns a single patient in an array

        x = GetRoutingSlip(host, port, token)
        x.setPatient(patients[17])
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue(len(ret[1]) == 1) 
        ret = ret[1][0]
        self.assertTrue("id" in ret)
        self.assertTrue("clinic" in ret)
        self.assertTrue(int(ret["clinic"] == clinicid))
        pid = int(ret["patient"])
        self.assertTrue(pid in patients)
        self.assertTrue(pid == patients[17])

        # search on patient and clinic, returns a single routing slip

        x = GetRoutingSlip(host, port, token)
        x.setPatient(patients[50])
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue(int(ret[1]["clinic"] == clinicid))
        pid = int(ret[1]["patient"])
        self.assertTrue(pid in patients)
        self.assertTrue(pid == patients[50])

        # search on bogus patient

        x = GetRoutingSlip(host, port, token)
        x.setPatient(9999)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # search on bogus clinic

        x = GetRoutingSlip(host, port, token)
        x.setPatient(patients[50])
        x.setClinic(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetRoutingSlip(host, port, token)
        x.setClinic(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        for i in routingslips:
            x = GetRoutingSlip(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == i)
            self.assertTrue(int(ret[1]["clinic"] == clinicid))
            pid = int(ret[1]["patient"])
            self.assertTrue(pid in patients)
            patients.remove(pid)

        self.assertTrue(len(patients) == 0)

        for i in routingslips:
            x = DeleteRoutingSlip(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

class TestTSRoutingSlipEntry(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateRoutingSlipEntry(self):
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
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipentryid = int(ret[1]["id"])

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 0))
        self.assertTrue(ret[1]["state"] == "Scheduled")

        x = DeleteRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipEntryBadClinicStation(self):
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
        stationid = int(ret[1]["id"])

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipEntryBadRoutingSlip(self):
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
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(9999)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinicStation(host, port, token, clinicstationid)
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
 
    def testDeleteRoutingSlipEntry(self):

        # create routingslip entry, delete, verify it is gone

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("Other")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipentryid = int(ret[1]["id"])

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 0))
        self.assertTrue(ret[1]["state"] == "Scheduled")

        x = DeleteRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # try deleting an invalid routingslip entry

        x = DeleteRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = CreateStation(host, port, token, "Ortho")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid1 = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid1 = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid2 = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid2 = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Speech")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid3 = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid3 = int(ret[1]["id"])

        ids = []
        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        for x in ids:
            y = GetRoutingSlipEntry(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == x)

        for x in ids:
            y = DeleteRoutingSlipEntry(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in ids:
            y = GetRoutingSlipEntry(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 404)

        x = DeleteClinicStation(host, port, token, clinicstationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, clinicstationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, clinicstationid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
    
    def testUpdateRoutingSlipEntry(self):
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
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipEntry(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipentryid = int(ret[1]["id"])

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 0))
        self.assertTrue(ret[1]["state"] == "Scheduled")

        x = UpdateRoutingSlipEntry(host, port, token, routingslipentryid)
        x.clearPayload()
        x.setState("Spaced Out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)   # can't checkout a patient in Scheduled state

        x = UpdateRoutingSlipEntry(host, port, token, routingslipentryid)
        x.clearPayload()
        x.setOrder(1)
        x.setState("Checked In")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 1))
        self.assertTrue(ret[1]["state"] == "Checked In")

        x = UpdateRoutingSlipEntry(host, port, token, routingslipentryid)
        x.clearPayload()
        x.setState("Checked Out")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 1))
        self.assertTrue(ret[1]["state"] == "Checked Out")

        x = UpdateRoutingSlipEntry(host, port, token, routingslipentryid)
        x.clearPayload()
        x.setOrder(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("clinicstation" in ret[1])
        self.assertTrue("state" in ret[1])
        self.assertTrue("order" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipentryid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["clinicstation"] == clinicstationid))
        self.assertTrue(int(ret[1]["order"] == 15))
        self.assertTrue(ret[1]["state"] == "Checked Out")

        x = UpdateRoutingSlipEntry(host, port, token, routingslipentryid)
        x.clearPayload()
        x.setState("Spaced Out")  # invalid state
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteRoutingSlipEntry(host, port, token, routingslipentryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllRoutingSlipEntry(self):

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        stationids = []
        clinicstationids = []
        routingslipentryids = []
        stations = ["ENT", "Speech", "Dental", "Ortho", "Screening"]
        for i in stations:
            x = CreateStation(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            stationid = int(ret[1]["id"])
            stationids.append(stationid)

            x = CreateClinicStation(host, port, token, clinicid, stationid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            clinicstationid = int(ret[1]["id"])
            clinicstationids.append(clinicstationid)

            x = CreateRoutingSlipEntry(host, port, token)
            x.setRoutingSlip(routingslipid)
            x.setClinicStation(clinicstationid)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            routingslipentryids.append(int(ret[1]["id"]))

        # search on routingslip, returns array

        x = GetRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]["routing"]), len(stations))

        # search on routingslip, returns array

        x = GetRoutingSlipEntry(host, port, token)
        x.setRoutingslip(routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        results = ret[1]
        self.assertTrue(len(results) == len(stations))
        for i in results:
            self.assertTrue(i in routingslipentryids)

        # search on clinicstation, returns single item 
   
        for i in clinicstationids: 
            x = GetRoutingSlipEntry(host, port, token)
            x.setRoutingslip(routingslipid)
            x.setClinicStation(i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            results = ret[1]
            self.assertTrue("routingslip" in results)
            self.assertTrue(results["routingslip"] == routingslipid)
            self.assertTrue("clinicstation" in results)
            self.assertTrue(results["clinicstation"] == i)

        # same thing, but don't pass routingslip
   
        for i in clinicstationids: 
            x = GetRoutingSlipEntry(host, port, token)
            x.setClinicStation(i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            results = ret[1]
            self.assertTrue(len(results) == 1)

        x = GetRoutingSlipEntry(host, port, token)
        x.setRoutingslip(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetRoutingSlipEntry(host, port, token)
        x.setClinicStation(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        for i in routingslipentryids:
            x = DeleteRoutingSlipEntry(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for i in clinicstationids:
            x = DeleteClinicStation(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for i in stationids:
            x = DeleteStation(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

class TestTSRoutingSlipComment(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        self.assertTrue("id" in ret[1])
        global token
        global userid
        token = ret[1]["token"]
        userid = int(ret[1]["id"])

    def testCreateRoutingSlipComment(self):
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
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setComment("Have a nice day")
        x.setAuthor(userid)                    
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipcommentid = int(ret[1]["id"])

        x = GetRoutingSlipComment(host, port, token, routingslipcommentid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("comment" in ret[1])
        self.assertTrue("author" in ret[1])
        self.assertTrue("updatetime" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipcommentid)
        self.assertTrue(int(ret[1]["comment"] == "Have a nice day"))
        self.assertTrue(int(ret[1]["author"]) == userid)

        x = DeleteRoutingSlipComment(host, port, token, routingslipcommentid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipCommentBadRoutingSlip(self):
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

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(9999)
        x.setComment("Have a nice day")
        x.setAuthor(userid)                    
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateRoutingSlipCommentBadAuthor(self):
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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(9999)
        x.setComment("Have a nice day")
        x.setAuthor(9999)                    
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
 
    def testCreateMultipleRoutingSlipComment(self):

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("New Cleft")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        routingslipcomments = []
        for i in xrange(0, 100):
            x = CreateRoutingSlipComment(host, port, token)
            x.setRoutingSlip(routingslipid)
            x.setComment("Comment {}".format(i))
            x.setAuthor(userid)                    
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            routingslipcomments.append(int(ret[1]["id"]))
        
        # search on routingslip, returns array

        x = GetRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertEqual(len(ret[1]["comments"]), 100)

        x = GetRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        results = ret[1]
        self.assertTrue(len(results) == len(routingslipcomments))

        for i in results:
            self.assertTrue(i in routingslipcomments)

        for i in routingslipcomments:
            x = GetRoutingSlipComment(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == i)
            self.assertTrue(int(ret[1]["author"] == userid))
            id = int(ret[1]["id"])
            self.assertTrue(ret[1]["comment"].find("Comment") != -1)
            self.assertTrue(id in routingslipcomments)

        for i in routingslipcomments:
            x = DeleteRoutingSlipComment(host, port, token, i)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteRoutingSlipComment(self):

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

        x = CreateRoutingSlip(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setCategory("Other")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipid = int(ret[1]["id"])

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setComment("Hello World!")
        x.setAuthor(userid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        routingslipcommentid = int(ret[1]["id"])

        x = GetRoutingSlipComment(host, port, token, routingslipcommentid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        self.assertTrue("routingslip" in ret[1])
        self.assertTrue("comment" in ret[1])
        self.assertTrue("author" in ret[1])
        self.assertTrue("updatetime" in ret[1])
        self.assertTrue(int(ret[1]["id"]) == routingslipcommentid)
        self.assertTrue(int(ret[1]["routingslip"] == routingslipid))
        self.assertTrue(int(ret[1]["author"] == userid))

        x = DeleteRoutingSlipComment(host, port, token, routingslipcommentid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRoutingSlipComment(host, port, token, routingslipcommentid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        ids = []
        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setComment("Another comment")
        x.setAuthor(userid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setComment("Yet Another comment")
        x.setAuthor(userid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        x = CreateRoutingSlipComment(host, port, token)
        x.setRoutingSlip(routingslipid)
        x.setComment("And yet another comment")
        x.setAuthor(userid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(int(ret[1]["id"]))

        for x in ids:
            y = GetRoutingSlipComment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            self.assertTrue(int(ret[1]["id"]) == x)

        for x in ids:
            y = DeleteRoutingSlipComment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in ids:
            y = GetRoutingSlipComment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 404)

        x = DeleteRoutingSlip(host, port, token, routingslipid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("routingslip [-h host] [-p port] [-u username] [-w password]") 

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
