'''
unit tests for ent treatment application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.patient.patient import CreatePatient, DeletePatient
from test.clinic.clinic import CreateClinic, DeleteClinic

class CreateENTTreatment(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateENTTreatment, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enttreatment/")

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)
    
    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)
    
    def setTreatment(self, val):
        self._payload["treatment"] = val 
        self.setPayload(self._payload)
    
    def setFuture(self, val):
        self._payload["future"] = val 
        self.setPayload(self._payload)
    
    def setSide(self, val):
        self._payload["side"] = val 
        self.setPayload(self._payload)
    
    def setComment(self, val):
        self._payload["comment"] = val 
        self.setPayload(self._payload)
    
    def setUsername(self, val):
        self._payload["username"] = val 
        self.setPayload(self._payload)
    
class GetENTTreatment(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/enttreatment/{}/".format(self._id)
        else:
            base = "tscharts/v1/enttreatment/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetENTTreatment, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._clinic = None
        self._patient = None
        self._id = None
        self.makeURL()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setClinic(self, val):
        self._clinic = val
        self.makeURL()

    def setPatient(self, val):
        self._patient = val
        self.makeURL()

    def setTreatment(self, val):
        self._treatment = val
        self.makeURL()

    def setSide(self, val):
        self._side = val
        self.makeURL()

    def setFuture(self, val):
        self._future = val
        self.makeURL()

class UpdateENTTreatment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateENTTreatment, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/enttreatment/{}/".format(id))

    def setClinic(self, val):
        self._payload["clinic"] = val
        self.setPayload(self._payload)

    def setPatient(self, val):
        self._payload["patient"] = val
        self.setPayload(self._payload)

    def setTreatment(self, val):
        self._payload["treatment"] = val
        self.setPayload(self._payload)

    def setFuture(self, val):
        self._payload["future"] = val
        self.setPayload(self._payload)

    def setSide(self, val):
        self._payload["side"] = val
        self.setPayload(self._payload)

    def setComment(self, val):
        self._payload["comment"] = val
        self.setPayload(self._payload)

    def setUsername(self, val):
        self._payload["username"] = val
        self.setPayload(self._payload)

class DeleteENTTreatment(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteENTTreatment, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/enttreatment/{}/".format(id))

class TestTSENTTreatment(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateENTTreatment(self):
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
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setTreatment("mastoid debrided")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        data = ret[1]

        self.assertTrue("treatment" in data)
        self.assertTrue(data["treatment"] == "mastoid debrided")
        self.assertTrue("side" in data)
        self.assertTrue(data["side"] == "right")
        self.assertTrue("future" in data)
        self.assertTrue(data["future"] == "true")
        self.assertTrue("comment" in data)
        self.assertTrue(data["comment"] == "A comment")
        self.assertTrue("username" in data)
        self.assertTrue(data["username"] == "Gomez")

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateENTTreatment(host, port, token)
        x.setClinic(9999)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # non-existent patient param

        x = CreateENTTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # no data

        x = CreateENTTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # invalid data

        x = CreateENTTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setTreatment("foobar")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # other requires a non-zero length name field

        x.setTreatment("other")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x.setTreatment("audiogram")
        x.setSide("oooo")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x.setTreatment("boric acid today")
        x.setSide("left")
        x.setFuture("jjjj")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
      
        # missing username 
        x = CreateENTTreatment(host, port, token)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setTreatment("tube removed")
        x.setSide("left")
        x.setFuture("false")
        x.setComment("A comment")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
       
        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteENTTreatment(self):
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
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setTreatment("antibiotic drops")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
       
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteENTTreatment(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTTreatment(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteENTTreatment(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTTreatment(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateENTTreatment(self):
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
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("false")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)

        x = UpdateENTTreatment(host, port, token, id)
        x.setTreatment("hearing aid eval")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["treatment"] == "hearing aid eval")

        x = UpdateENTTreatment(host, port, token, id)
        x.setTreatment("other")
        x.setComment("Itchy Scratchy")
        x.setSide("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = UpdateENTTreatment(host, port, token, id)
        x.setClinic(clinicid)
        x.setPatient(patientid)
        x.setSide("both")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("patient" in ret[1])
        patientId = int(ret[1]["patient"])
        self.assertTrue(patientId == patientid)
        self.assertTrue(ret[1]["treatment"] == "other")
        self.assertTrue(ret[1]["side"] == "both")
        self.assertTrue(ret[1]["comment"] == "Itchy Scratchy")

        x = UpdateENTTreatment(host, port, token, id)
        x.setTreatment("other")
        x.setComment("")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = UpdateENTTreatment(host, port, token, id)
        x.setTreatment("cleaned")
        x.setSide("yadda")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteENTTreatment(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllENTHistories(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid1 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "05/05/2016", "05/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid2 = int(ret[1]["id"])

        x = CreateClinic(host, port, token, "Ensenada", "08/05/2016", "08/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid3 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "3abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid1 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "1abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "2abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
        data["street1"] = "1234 First Ave"
        data["street2"] = ""
        data["city"] = "Ensenada"
        data["colonia"] = ""
        data["state"] = u"Baja California"
        data["phone1"] = "1-111-111-1111"
        data["phone2"] = ""
        data["email"] = "patient@example.com"
        data["emergencyfullname"] = "Maria Sanchez"
        data["emergencyphone"] = "1-222-222-2222"
        data["emergencyemail"] = "maria.sanchez@example.com"

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        delids = []

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid1)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid1)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid1)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid2)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")

        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid2)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid3) 
        x.setClinic(clinicid2)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid1)
        x.setClinic(clinicid3)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid2)
        x.setClinic(clinicid3)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = CreateENTTreatment(host, port, token)
        x.setPatient(patientid3)
        x.setClinic(clinicid3)
        x.setTreatment("cleaned")
        x.setSide("right")
        x.setFuture("true")
        x.setComment("A comment")
        x.setUsername("Gomez")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        delids.append(ret[1]["id"])

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        x = GetENTTreatment(host, port, token)
        x.setPatient(patientid3)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 3)

        for x in delids:
            y = DeleteENTTreatment(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetENTTreatment(host, port, token)
        x.setClinic(clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        rtcs = ret[1]
        self.assertTrue(len(rtcs) == 0)

        x = DeleteClinic(host, port, token, clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid2)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid3)
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

def usage():
    print("enttreatment [-h host] [-p port] [-u username] [-w password]") 

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
