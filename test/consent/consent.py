'''
unit tests for consent application. Assumes django server is up
and running on the specific host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.patient.patient import CreatePatient, DeletePatient
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.register.register import CreateRegistration, GetRegistration, UpdateRegistration, DeleteRegistration

class CreateConsent(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreateConsent, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/consent/")

class GetConsent(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/consent/{}/".format(self._id)
        else:
            base = "tscharts/v1/consent/"

        if not self._registrationid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "register={}".format(self._registrationid)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetConsent, self).__init__()

        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._id = None
        self._registrationid = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setRegistration(self, register):
        self._registrationid = register
        self.makeURL()

class DeleteConsent(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteConsent, self).__init__()

        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/consent/{}/".format(id))

class testTSConsent(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateConsent(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid = int(ret[1]["id"])

        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        data["photo_consent"] = True
        
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        #get consent with consent id
        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertTrue("register" in ret[1])
        registrationId = int(ret[1]["register"])
        self.assertTrue(registrationId == registrationid)

        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == True)
            
        #get consent with registration id
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("register" in ret[1])
        registrationId = int(ret[1]["register"])
        self.assertTrue(registrationid == registrationId)
        
        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == True)


        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) #non-exist after delete

        #non-exist register
        data = {}
        data["register"] = 9999
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #invalid data boolean argu
        data = {}
        data["register"] = registrationid
        data["general_consent"] = 123
        data["photo_consent"] = 456
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["register"] = registrationid
        data["general_consent"] = "hello"
        data["photo_consent"] = "world"
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        #invalid field name        
        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        data["photo_consent"] = False
        data["hello_world"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        #not contain all the required fields
        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        #duplicate consent info with same registration
        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        data["photo_consent"] = False
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        id = int(ret[1]["id"])

        data = {}
        data["register"] = registrationid
        data["general_consent"] = False
        data["photo_consent"] = True
        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)


        #delete registration, patient, clinic
        x = DeleteRegistration(host, port, token, registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)


    def testDeleteConsent(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid = int(ret[1]["id"])

        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        data["photo_consent"] = True

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404) #not found

        x = DeleteConsent(host, port, token, 9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteConsent(host, port, token, None)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteConsent(host, port, token, "")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        x = DeleteConsent(host, port, token, "Hello")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteRegistration(host, port, token, registrationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetConsent(self):
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

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid = int(ret[1]["id"])

        data = {}
        data["register"] = registrationid
        data["general_consent"] = True
        data["photo_consent"] = False

        x = CreateConsent(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        #get consent with consent id
        x = GetConsent(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertTrue("register" in ret[1])
        registrationId = int(ret[1]["register"])
        self.assertTrue(registrationId == registrationid)

        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)


        #get consent with registration id
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("register" in ret[1])
        registrationId = int(ret[1]["register"])
        self.assertTrue(registrationid == registrationId)

        data = ret[1]
        self.assertTrue("general_consent" in data)
        self.assertTrue("photo_consent" in data)

        self.assertTrue(data["general_consent"] == True)
        self.assertTrue(data["photo_consent"] == False)

        #get consent with non-exist consent id
        x = GetConsent(host, port, token)
        x.setId(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        #get consent with non-exist registration id
        x = GetConsent(host, port, token)
        x.setRegistration(9999)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        x = CreateClinic(host, port, token, "Ensenada", "02/08/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid1 = int(ret[1]["id"])

        x = CreateRegistration(host, port, token, patient=patientid, clinic=clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        registrationid1 = int(ret[1]["id"])
    
        #get consent with a registration id that exists but no consent info corresponds with it
        x = GetConsent(host, port, token)
        x.setRegistration(registrationid1)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 404)

        x = DeleteConsent(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRegistration(host, port, token, registrationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteRegistration(host, port, token, registrationid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid1)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)


def usage():
    print("surgeryhistory [-h host] [-p port] [-u username] [-w password]") 

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
