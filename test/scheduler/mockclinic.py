#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2017
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

import unittest
import getopt, sys
import json
from datetime import datetime, timedelta
from random import randint
import time

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.station.station import CreateStation, DeleteStation, GetStation
from test.patient.patient import CreatePatient, DeletePatient
from test.clinicstation.clinicstation import CreateClinicStation, DeleteClinicStation
from test.routingslip.routingslip import CreateRoutingSlip, UpdateRoutingSlip, GetRoutingSlip, DeleteRoutingSlip, CreateRoutingSlipEntry, GetRoutingSlipEntry, UpdateRoutingSlipEntry, DeleteRoutingSlipEntry

class MockClinic: 
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._clinicid = None
        self._stationids = []
        self._clinicstationids = []
        self._patientids = []
        self._routingslipids = []
        self._routingslipentryids = []

        self._categories = ["New Cleft", "Dental", "Returning Cleft", "Ortho", "Other"]

    def login(self):
        retval = True

        login = Login(self._host, self._port, self._username, self._password)
        ret = login.send(timeout=30)
        if ret[0] == 200:
            self._token = ret[1]["token"]
        else:
            print("unable to login")
            retval = False
        return retval
        
    def logout(self):
        logout = Logout(self._host, self._port)
        ret = logout.send(timeout=30)

    def getPatients(self):
        return self._patientids

    def getClinic(self):
        return self._clinicid

    def getStations(self):
        return self._stationids

    def getStationName(self, station):
        retval = None
        x = GetStation(self._host, self._port, self._token, station)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            retval = ret[1]["name"]
        else:
            print("unable to get data for station {}".format(station))
        return retval

    def createClinic(self, location):
        # create clinic that is occurring today, since scheduler will only
        # process a clinic that is currently active.

        retval = None

        today = datetime.utcnow().strftime("%m/%d/%Y")
        todayplusone = (datetime.utcnow() + timedelta(hours=24)).strftime("%m/%d/%Y")
        x = CreateClinic(self._host, self._port, self._token, location, today, todayplusone)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinic {} {} {}".format(location, today, todayplusone))
        else:
            self._clinicid = ret[1]["id"]
            retval = self._clinicid
        return retval

    def createStation(self, name):
        retval = None
        x = CreateStation(self._host, self._port, self._token, name)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create station {}".format(name))
        else:
            self._stationids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createClinicStation(self, clinicid, stationid, name):
        retval = None        
        x = CreateClinicStation(self._host, self._port, self._token, clinicid, stationid, name=name)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinicstation {}".format(name))
        else:
            self._clinicstationids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createPatient(self, data):
        retval = None
        x = CreatePatient(self._host, self._port, self._token, data)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create patient {}".format(data))
        else:
            self._patientids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createRoutingSlip(self, patient, clinic, category):
        retval = None
        if not patient in self._patientids:
            print("failed to create routingslip invalid patient {}".format(patient))
        elif clinic != self._clinicid:
            print("failed to create routingslip invalid clinic {}".format(clinic))
        else:
            x = CreateRoutingSlip(self._host, self._port, self._token)
            x.setClinic(clinic)
            x.setPatient(patient)
            x.setCategory(category)
            ret = x.send(timeout=30)
            if ret[0] != 200:
                print("failed to create routingslip patient {} clinic {} category {}".format(patient, clinic, category))
            else:
                self._routingslipids.append(int(ret[1]["id"]))
                retval = int(ret[1]["id"])
        return retval

    def createRoutingSlipEntry(self, routingslip, station):
        retval = None
        if not routingslip in self._routingslipids:
            print("failed to create routingslip entry invalid routingslip {}".format(routingslip))
        elif not station in self._stationids:
            print("failed to create routingslip entry invalid station {}".format(station))
        else:
            x = CreateRoutingSlipEntry(self._host, self._port, self._token)
            x.setRoutingSlip(routingslip)
            x.setStation(station)
            ret = x.send(timeout=30)
            if ret[0] != 200:
                print("failed to create routingslip entry routingslip {} station {}".format(routingslip, station))
            else:
                self._routingslipentryids.append(int(ret[1]["id"]))
                retval = int(ret[1]["id"])
        return retval

    def getRandomCategory(self):
        return self._categories[randint(0, len(self._categories)) - 1]    

    def createAllPatients(self, count):
        for i in xrange(0, count):
            data = {}
            data["paternal_last"] = "{}abcd1234".format(i)
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
            self.createPatient(data)

    def createClinicResources(self):
        print("Creating clinic")
        clinic = self.createClinic("Ensenada")
        print("Creating stations")
        dental = self.createStation("Dental")
        ent = self.createStation("ENT")
        ortho = self.createStation("Ortho") 
        xray = self.createStation("X-Ray") 
        surgery = self.createStation("Surgery Screening") 
        speech = self.createStation("Speech") 
        audiology = self.createStation("Audiology") 

        dentalStations = []
        for x in ["Dental1", "Dental2", "Dental3", "Dental4", "Dental5"]:
            print("Creating station {}".format(x))
            dentalStations.append(self.createClinicStation(clinic, dental, x))
        entStation = self.createClinicStation(clinic, ent, "ENT") 
        print("Creating station {}".format("ENT"))
        orthoStations = []
        for x in ["Ortho1", "Ortho2"]:
            print("Creating station {}".format(x))
            orthoStations.append(self.createClinicStation(clinic, ortho, x))
        print("Creating station {}".format("X-Ray"))
        xrayStation = self.createClinicStation(clinic, xray, "X-Ray") 
        print("Creating station {}".format("Surgery Screening"))
        surgeryStation = self.createClinicStation(clinic, surgery, "Surgery Screening") 
        print("Creating station {}".format("Speech"))
        speechStation = self.createClinicStation(clinic, speech, "Speech") 
        print("Creating station {}".format("Audiology"))
        audiologyStation = self.createClinicStation(clinic, audiology, "Audiology") 

def usage():
    print("mockclinic [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    host = "127.0.0.1"
    port = 8000
    username = None
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

    mock = MockClinic(host, port, username, password)   
    if mock.login():
        mock.createClinicResources()
        clinic = mock.getClinic()
        n = randint(50, 100)
        print("Registering {} patients for this clinic".format(n))
        mock.createAllPatients(n)
        for x in mock.getPatients():
            time.sleep(randint(1, 30))
            cat = mock.getRandomCategory()
            routingslip = mock.createRoutingSlip(x, clinic, cat)
            print("\n\nCreating routingslip for {} patient {} at UTC time {}".format(cat, x, datetime.utcnow().strftime("%H:%M:%S")))
            for y in mock.getStations():
                if randint(0, 1) == 1:
                    print("Adding station {} to routing slip".format(mock.getStationName(y)))
                    mock.createRoutingSlipEntry(routingslip, y)    
        mock.logout()

if __name__ == "__main__":
    main()
