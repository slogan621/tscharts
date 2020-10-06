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
unit tests for image application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json
from random import randint

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.station.station import CreateStation, DeleteStation
from tschartslib.patient.patient import CreatePatient, DeletePatient

class CreateImage(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateImage, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/image/")       

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)
    
    def setStation(self, station):
        self._payload["station"] = station
        self.setPayload(self._payload)
    
    def setPatient(self, patient):
        self._payload["patient"] = patient
        self.setPayload(self._payload)
    
    def setData(self, data):
        self._payload["data"] = data
        self.setPayload(self._payload)
    
    def setType(self, imagetype):
        self._payload["type"] = imagetype
        self.setPayload(self._payload)
    
class GetImage(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetImage, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._clinic = None
        self._station = None
        self._patient = None
        self._type = None
        self._id = None
        self._sort = None
        self._newest = None
        self.makeURL();

    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/image/{}/".format(self._id)
        else:
            base = "tscharts/v1/image/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._station == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "station={}".format(self._station)
            hasQArgs = True

        if not self._patient == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patient={}".format(self._patient)
            hasQArgs = True

        if not self._type == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "type={}".format(self._type)
            hasQArgs = True

        if not self._newest == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "newest={}".format(self._newest)
            hasQArgs = True

        if not self._sort == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "sort={}".format(self._sort)
            hasQArgs = True

        self.setURL(base)

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setNewest(self, val):
        self._newest = val
        self.makeURL()

    def setStation(self, station):
        self._station = station
        self.makeURL()
    
    def setPatient(self, patient):
        self._patient = patient
        self.makeURL()
    
    def setType(self, imagetype):
        self._type = imagetype
        self.makeURL()
    
    def setSort(self, sort):
        self._sort = sort
        self.makeURL()
    
class DeleteImage(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteImage, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/image/{}/".format(id))

class TestTSImage(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateImage(self):
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

        for imageType in ["Xray", "Headshot", "Audiogram", "Surgery"]:

            x = CreateImage(host, port, token)
            x.setPatient(patientid)
            x.setClinic(clinicid)
            x.setStation(stationid)
            x.setType(imageType)
            x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            id = int(ret[1]["id"])
            x = GetImage(host, port, token)
            x.setId(id)
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
            self.assertTrue("type" in ret[1])
            self.assertTrue(ret[1]["type"] == imageType)
            self.assertTrue("data" in ret[1])
            self.assertTrue(ret[1]["data"] == "ABCDEFG")

            x = DeleteImage(host, port, token, id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            x = GetImage(host, port, token)
            x.setId(id)
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(99999)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        x.setStation(stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setStation(9999)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent patient param

        x = CreateImage(host, port, token)
        x.setPatient(9999)
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # bogus clinic param

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic("fffff")
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # bogus station param

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setStation(None)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # bogus patient param

        x = CreateImage(host, port, token)
        x.setPatient("")
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # missing patient

        x = CreateImage(host, port, token)
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # missing clinic

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # missing station

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # Wrong type

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Bad Type")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # Missing Data

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Headshot")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteImage(self):
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

        x = CreateImage(host, port, token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setStation(stationid)
        x.setType("Headshot")
        x.setData("ABCDEFG")    # doesn't matter if it is actual image data 
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetImage(host, port, token)
        x.setId(id)
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
        self.assertTrue("type" in ret[1])
        self.assertTrue(ret[1]["type"] == "Headshot")
        self.assertTrue("data" in ret[1])
        self.assertTrue(ret[1]["data"] == "ABCDEFG")

        x = DeleteImage(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetImage(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteImage(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteImage(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteImage(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteImage(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllImages(self):
        clinics = []
        stations = []
        patients = []
        images = []

        nclinics = 3
        nstations = 4
        npatients = 5
        nimages = 1

        for i in xrange(1, nclinics + 1):
            x = CreateClinic(host, port, token, "Ensenada", "{}/05/2016".format(i), "{}/06/2016".format(i))
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            self.assertTrue("id" in ret[1])
            clinics.append(int(ret[1]["id"]))

        for j in xrange(1, nstations + 1):
            x = CreateStation(host, port, token, "Dental{}".format(j))
            ret = x.send(timeout=30)
            self.assertEqual(ret[0], 200)
            stations.append(int(ret[1]["id"]))

        for k in range(1, npatients + 1):
            data = {}
            data["paternal_last"] = "abcd1234{}".format(k) 
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
            patients.append(int(ret[1]["id"]))

        for i in clinics:
            for j in stations:
                for k in patients: 
                    for l in xrange(0, nimages):
                        x = CreateImage(host, port, token)
                        x.setPatient(k)
                        x.setClinic(i)
                        x.setStation(j)
                        x.setType("Headshot")
                        x.setData("ABCDEFG{}".format(l))  
                        ret = x.send(timeout=30)
                        self.assertEqual(ret[0], 200)
                        images.append(int(ret[1]["id"]))

        # query by invalid search terms
        x = GetImage(host, port, token)
        x.setClinic(9999)
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setType("Headshot")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(9999)
        x.setPatient(patients[0])
        x.setType("Headshot")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(9999)
        x.setType("Headshot")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setType("yadda")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setSort("yadda")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setSort("False")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setSort("True")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setSort("false")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetImage(host, port, token)
        x.setClinic(clinics[0])
        x.setStation(stations[0])
        x.setPatient(patients[0])
        x.setSort("true")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        sort = "true"
        for c in clinics:
            for s in stations:
                for p in patients:
                    if sort =="true":
                        sort = "false"
                    else:
                        sort = "true"
                    # query by type
                    x = GetImage(host, port, token)
                    x.setPatient(p)
                    x.setSort(sort)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    # query by clinic
                    x = GetImage(host, port, token)
                    x.setClinic(c)
                    x.setSort(sort)
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == len(images) / nclinics)
                    # query by clinic and type
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == len(images) / nclinics)
                    # query by station
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setStation(s)
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == (len(images) / nstations))
                    # query by station and type
                    x = GetImage(host, port, token)
                    x.setStation(s)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    # query by clinic and station
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setStation(s)
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == len(images) / (nclinics * nstations))
                    # query by clinic, station and type
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setStation(s)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    # query by clinic and patient
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setPatient(p)
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == len(images) / (nclinics * npatients))
                    # query by clinic, patient and type
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setPatient(p)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    # query by clinic, station, and patient
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setStation(s)
                    x.setPatient(p)
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)
                    self.assertTrue(len(ret[1]) == len(images) / (nclinics * nstations * npatients))
                    # query by clinic, station, patient and type
                    x = GetImage(host, port, token)
                    x.setSort(sort)
                    x.setClinic(c)
                    x.setStation(s)
                    x.setPatient(p)
                    x.setType("Headshot")
                    ret = x.send(timeout=30)
                    self.assertEqual(ret[0], 200)

        for x in images:
            y = DeleteImage(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in patients:
            y = DeletePatient(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in stations:
            y = DeleteStation(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        for x in clinics:
            y = DeleteClinic(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

def usage():
    print("image [-h host] [-p port] [-u username] [-w password]") 

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
