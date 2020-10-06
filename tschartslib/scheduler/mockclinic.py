# -*- coding: utf-8 -*-

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

import unittest
import getopt, sys
import json
from datetime import datetime, timedelta
from random import randint
import time
import threading
import base64

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.clinic.clinic import CreateClinic, DeleteClinic
from tschartslib.queue.queue import GetQueue, DeleteQueueEntry
from tschartslib.category.category import CreateCategory
from tschartslib.image.image import CreateImage
from tschartslib.station.station import CreateStation, DeleteStation, GetStation
from tschartslib.patient.patient import CreatePatient, DeletePatient
from tschartslib.returntoclinic.returntoclinic import CreateReturnToClinic
from tschartslib.medicalhistory.medicalhistory import CreateMedicalHistory, DeleteMedicalHistory
from tschartslib.xray.xray import CreateXRay, DeleteXRay
from tschartslib.register.register import CreateRegistration
from tschartslib.statechange.statechange import CreateStateChange
from tschartslib.returntoclinicstation.returntoclinicstation import CreateReturnToClinicStation, GetReturnToClinicStation, UpdateReturnToClinicStation
from tschartslib.clinicstation.clinicstation import CreateClinicStation, DeleteClinicStation, UpdateClinicStation, GetClinicStation
from tschartslib.routingslip.routingslip import CreateRoutingSlip, UpdateRoutingSlip, GetRoutingSlip, DeleteRoutingSlip, CreateRoutingSlipEntry, GetRoutingSlipEntry, UpdateRoutingSlipEntry, DeleteRoutingSlipEntry
import random

def awayWorker(mc):
    clinicstations = mc._clinicstationids 
    random.shuffle(clinicstations)
    for x in clinicstations:
        time.sleep(randint(60, 300))
        busy = True
        while busy == True:
            time.sleep(5)
            y = GetClinicStation(mc._host, mc._port, mc._token)
            y.setId(x)
            ret = y.send(timeout=30)
            if ret[0] == 200:
                if ret[1]["active"] == False:
                    break
        y = UpdateClinicStation(mc._host, mc._port, mc._token, x)
        y.setActive(False)
        awaytime = randint(1, 5)
        y.setAwayTime(awaytime)
        y.setAway(True)
        ret = y.send(timeout=30)
        if ret[0] == 200:
            time.sleep(awaytime * 60)
            y.setAway(False)
            ret = y.send(timeout=30)

def hasReturnToClinicStation(mockclinic, clinicid, patientid):
    retval = False

    host = mockclinic._host
    port = mockclinic._port
    token = mockclinic._token   

    x = GetReturnToClinicStation(host, port, token)
    x.setClinic(clinicid)
    x.setPatient(patientid)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        if len(ret[1]) > 0:
            retval = True
    return retval

def inRoutingSlip(mockclinic, clinicid, patientid, stationid):
    retval = False
    host = mockclinic._host
    port = mockclinic._port
    token = mockclinic._token   

    x = GetRoutingSlip(host, port, token)
    x.setClinic(clinicid)
    x.setPatient(patientid)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        entries = ret[1]["routing"]
        for entry in entries:
            x = GetRoutingSlipEntry(host, port, token)
            x.setId(entry)
            ret = x.send(timeout=30)
            if ret[0] == 200:
                station = ret[1]["station"]
                if station == stationid:
                    retval = True
                    break
            else:
                print("inRoutingSlip failed to get routing slip entry {} return {}".format(entry, ret[0]))
    else:       
        print("inRoutingSlip failed to get routing slip for clinic {} patient {} return {}".format(clinicid, patientid, ret[0]))
    return retval    

def checkAndUpdateScheduledDestReturnToClinicStation(mockclinic, clinicid, patientid, stationid):
    retval = False

    host = mockclinic._host
    port = mockclinic._port
    token = mockclinic._token   

    x = GetReturnToClinicStation(host, port, token)
    x.setClinic(clinicid)
    x.setStation(stationid)
    x.setPatient(patientid)
    x.setState("scheduled_dest")
    ret = x.send(timeout=30)
    if ret[0] == 200:
        if len(ret[1]) > 1:
            print("checkAndUpdateScheduledDestReturnToClinicStation: found more than one ({}) returntoclinicstation for clinic {} patient {} station {}".format(len(ret[1]), clinicid, patientid, stationid))
        elif len(ret[1]) == 0:
            print("checkAndUpdateScheduledDestReturnToClinicStation: success returned but empty list returntoclinicstation for clinic {} patient {} station {}".format(clinicid, patientid, stationid))
        else:
            rtcsid = ret[1][0]["id"]
            x = UpdateReturnToClinicStation(host, port, token, rtcsid)
            x.setState("checked_out_dest")
            ret = x.send(timeout=30)
            if ret[0] != 200:
                print("checkAndUpdateScheduledDestReturnToClinicStation: failed to put returntoclinicstation {} for clinic {} patient {} station {} into checked_out_dest state. return code {}".format(rtcsid, clinicid, patientid, stationid, ret[0]))
            else:
                print("checkAndUpdateScheduledDestReturnToClinicStation: put returntoclinicstation {} for clinic {} patient {} station {} into checked_out_dest state. return code {}".format(rtcsid, clinicid, patientid, stationid, ret[0]))
                retval = True
    else:
        print("checkAndUpdateScheduledDestReturnToClinicStation: failed to get returntoclinicstation for clinic {} patient {} station {}. return {}".format(clinicid, patientid, stationid, ret[0]))
    return retval

def checkinWorker(clinicstationid, mockclinic):
    print("checkinWorker starting thread for clinic station {}".format(clinicstationid))
    host = mockclinic._host
    port = mockclinic._port
    token = mockclinic._token   
    doReturnToClinicStation = mockclinic._doReturnToClinicStation
    clinicid = mockclinic.getClinic() 
    clinicstations = mockclinic.getClinicStations()
    stations = mockclinic.getStations()
    while True:
        time.sleep(randint(1, 30))
        # get queue for this clinicstation 
        # if item in queue, checkin the patient, work for some
        # random amount of time, then check out
    
        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            if ret[1]["away"] == True:
                continue
        else:
            print("checkinWorker: unable to get clinicstation {} ret {}".format(clinicstationid, ret[0]))
        
        try:    
            stationid = ret[1]["station"] # used to find returntoclinicstation matches
        except:
            print("checkinWorker: unable to get station for clinicstation {}".format(clinicstationid))
            continue

        x = GetQueue(host, port, token)
        x.setClinic(clinicid)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        if ret[0] == 200 and len(ret[1]["queues"]) > 0:
            try:
                print("checkinWorker: query queues for clinicstation {} got {}".format(clinicstationid, ret[1]))
                entries = ret[1]["queues"][0]["entries"]
                if len(entries):
                    # something in the queue
                    entry = entries[0]
                    q = DeleteQueueEntry(host, port, token)
                    q.setQueueEntryId(entry["id"])
                    ret = q.send(timeout=30)
                    if ret[0] == 200:
                        print("checkinWorker: deleted queueentry {}".format(entry["id"]))
                        y = UpdateClinicStation(host, port, token, clinicstationid)
                        y.setActive(True)
                        y.setActivePatient(entry["patient"])
                        ret = y.send(timeout=30)
                        if ret[0] == 200:
                            print("checkinWorker: set clinicstation {} active patient to {}".format(clinicstationid, entry["patient"]))
                            z = UpdateRoutingSlipEntry(host, port, token, entry["routingslipentry"])
                            z.setState("Checked In")
                            ret = z.send(timeout=30)
                            if ret[0] == 200:
                                print("checkinWorker: clinicstation {} checked in patient {}".format(clinicstationid, entry["patient"]))
                                r = CreateStateChange(host, port, token)
                                r.setClinicStation(clinicstationid)
                                r.setPatient(entry["patient"])
                                r.setState("in")
                                ret = r.send(timeout=30)
                                if ret[0] == 200:
                                    # do some work
                                    t = randint(120, 180)
                                    print("checkinWorker: clinicstation {} starting work on patient {} for {} seconds".format(clinicstationid, entry["patient"], t))
                                    time.sleep(t)

                                    '''
                                    check for a returntoclinicstation object
                                    that is in state scheduled_dest and matches
                                    our station type and patient for this
                                    clinic. If found, update the state of the
                                    returntoclinicstation object to 
                                    checked_out_dest.
                                    '''

                                    success = checkAndUpdateScheduledDestReturnToClinicStation(mockclinic, clinicid, entry["patient"], stationid)

                                    if not hasReturnToClinicStation(mockclinic, clinicid, entry["patient"]) and randint(0, 1) == 1 and doReturnToClinicStation == True:
                                        o = randint(1, len(stations))
                                        if o != stationid and not inRoutingSlip(mockclinic, clinicid, entry["patient"], o):
                                            try:              
                                                # create returntoclinicstation 
                                                print("checkinWorker: Creating return to clinicstation record")
                                                rtc = CreateReturnToClinicStation(host, port, token, clinicid, entry["patient"], o, clinicstationid)

                                                ret = rtc.send(timeout=30)
                                                if ret[0] != 200:
                                                    print("checkinWorker: Unable to create return to clinicstation object. clinic {} patient {} station {} clinicstation {} ret is {}".format(clinicid, entry["patient"], o, clinicstationid, ret[0]))
                                                    sys.exit(1)
                                                else:
                                                    print("checkinWorker: Created return to clinicstation object")
                                            except Exception as e:
                                                msg = sys.exc_info()[0]
                                                print("checkinWorker: exception creating return to clinic {}: {}".format(ret[1], msg))
                                                sys.exit(1)

                                    # check the patient out

                                    z.setState("Checked Out")
                                    ret = z.send(timeout=30)
                                    if ret[0] == 200:
                                        print("checkinWorker: clinicstation {} checked out patient {}".format(clinicstationid, entry["patient"]))
                                        r.setState("out")
                                        ret = r.send(timeout=30)
                                        if ret[0] == 200:
                                            y.setActive(False)
                                            ret = y.send(timeout=30)
                                            if ret[0] == 200:
                                                print("checkinWorker: set clinicstation {} active state to False".format(clinicstationid))
                                            else:
                                                print("checkinWorker: failed to set clinicstation active to false {}".format(ret[0]))
                                        else:
                                            print("checkinWorker: failed to create statechange record for state 'out' {}".format(ret[0]))
                                    else:
                                        print("checkinWorker: failed to set state to 'Checked Out' {}".format(ret[0]))
                                else:
                                    print("checkinWorker: failed to create statechange record for state 'in' {}".format(ret[0]))
                            else:
                                print("checkinWorker: failed to set state to 'Checked In' {}".format(ret[0]))
                        else:
                            print("checkinWorker: failed to set clinicstation active patient id {} : {}".format(entry["patient"], ret[0]))
                    else: 
                        print("checkinWorker: failed to delete queue entry {}  {}".format(entry["id"], ret[0]))
                else:
                    print("checkinWorker: no waiting entries for clinicstation {}".format(clinicstationid))
            except Exception as e:
                msg = sys.exc_info()[0]
                print("checkinWorker: exception {}: {}".format(ret[1], msg))
                sys.exit(1)
        else:
            print("checkinWorker: failed to get queue entry for clinicstation {}: {}".format(clinicstationid, ret[0]))

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

        self._categories = ["New Cleft", "Dental", "Returning Cleft", "Ortho", "Hearing Aids", "Ears", "Other"]
        self._doReturnToClinicStation = False 

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

    def simulateCheckins(self):
        # create a thread for each station and then perform checkins, simulated
        # service for some random duration, then checkouts while there are still
        # patients waiting to be seen
        threads = []
        for x in self._clinicstationids:
            t = threading.Thread(target=checkinWorker, args=(x,self,))
            t.daemon = True
            t.start()
            threads.append(t)
        return threads

    def simulateAway(self):
        t = threading.Thread(target=awayWorker, args=(self,))
        t.daemon = True
        t.start()

    def getClinic(self):
        return self._clinicid

    def getStations(self):
        return self._stationids

    def getClinicStations(self):
        return self._clinicstationids

    def getStationName(self, station):
        retval = None
        x = GetStation(self._host, self._port, self._token, station)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            retval = ret[1]["name"]
        else:
            print("unable to get data for station {}".format(station))
        return retval
        
    def getQueue(self, clinicstationid):
        pass

    def createRegistration(self, clinicid, patientid):
        x = CreateRegistration(self._host, self._port, self._token, clinic=clinicid, patient=patientid)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinic {} registration for patient {} {}".format(clinicid, patientid, x))

    def createReturnToClinic(self, patientid, clinicid, stationid, interval):
        x = CreateReturnToClinic(self._host, self._port, self._token, patient=patientid, clinic=clinicid, station=stationid, interval=interval)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create return to clinic {}".format(x))

    def createCategories(self, cats = None):
        if cats != None:
            self._categories = cats
        for x in self._categories:
            data = {}
            data["name"] = x
            r = CreateCategory(self._host, self._port, self._token, data)
            ret = r.send(timeout=30)
            if ret[0] != 200:
                print("failed to create category {}".format(x))

    def createClinic(self, location="Ensenada", duration=1):
        # create clinic that is occurring today, since scheduler will only
        # process a clinic that is currently active.

        retval = None

        today = datetime.now().strftime("%m/%d/%Y")
        todayplusone = (datetime.now() + timedelta(hours=24 * (duration - 1))).strftime("%m/%d/%Y")
        x = CreateClinic(self._host, self._port, self._token, location, today, todayplusone)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinic {} {} {}".format(location, today, todayplusone))
        else:
            self._clinicid = ret[1]["id"]
            retval = self._clinicid
        return retval

    def createStation(self, name, level):
        retval = None
        x = CreateStation(self._host, self._port, self._token, name, level)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create station {}".format(name))
        else:
            self._stationids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createClinicStation(self, clinicid, stationid, name):
        retval = None        
        away = False
        active = False
        print("Creating clinicstation {} away {} active {}".format(name[0], away, active))
        x = CreateClinicStation(self._host, self._port, self._token, clinicid, stationid, name=name[0], name_es=name[1], away=away, active=active)
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

    def simulateReturnToClinicStation(self, doReturnToClinicStation):
        self._doReturnToClinicStation = doReturnToClinicStation

    def getRandomCategory(self):
        return self._categories[randint(0, len(self._categories)) - 1]    

    def randomBoolean(self):   
        ret = True
        x = randint(0, 1)
        if x == 0:
            ret = False
        return ret;

    def addPhoto(self, clinicid, genderStr, patientid):
        # figure out what image to use

        ret = self.randomBoolean()
        if ret == False: 
            return

        imageid = patientid % 10
        if genderStr == "Female":
            image = "images/girlfront-{}.jpg".format(imageid);
        else:
            image = "images/boyfront-{}.jpg".format(imageid);

        # load it, and base64 encode it

        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        x = CreateImage(self._host, self._port, self._token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setType("Headshot")
        x.setData(encoded_string)  
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to create patient headshot photo clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))

    def createXRay(self, clinicid, patientid):    
        x = CreateXRay(self._host, self._port, self._token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setMouthType("child")
        x.setTeeth(randint(0, 15))
        r = self.randomBoolean()
        if r == True:
            x.setXRayType("full")
        else:
            x.setXRayType("anteriors_bitewings")
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to create XRay clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))

    def createMedicalHistory(self, clinicid, patientid):    
        x = CreateMedicalHistory(self._host, self._port, self._token, patient=patientid, clinic=clinicid)

        data = {}
        data["cold_cough_fever"] = self.randomBoolean()
        data["hivaids"] = self.randomBoolean()
        data["anemia"] = self.randomBoolean()
        data["athsma"] = self.randomBoolean()
        data["cancer"] = self.randomBoolean()
        data["congenitalheartdefect"] = self.randomBoolean()
        data["congenitalheartdefect_workup"] = self.randomBoolean()
        data["congenitalheartdefect_planforcare"] = self.randomBoolean()
        data["diabetes"] = self.randomBoolean()
        data["epilepsy"] = self.randomBoolean()
        data["bleeding_problems"] = self.randomBoolean()
        data["hepititis"] = self.randomBoolean()
        data["tuberculosis"] = self.randomBoolean()
        data["troublespeaking"] = self.randomBoolean()
        data["troublehearing"] = self.randomBoolean()
        data["troubleeating"] = self.randomBoolean()
        data["pregnancy_duration"] = randint(6, 9)
        data["pregnancy_smoke"] = self.randomBoolean()
        data["birth_complications"] = self.randomBoolean()
        data["pregnancy_complications"] = self.randomBoolean()
        data["mother_alcohol"] = self.randomBoolean()
        data["relative_cleft"] = self.randomBoolean()
        data["parents_cleft"] = self.randomBoolean()
        data["siblings_cleft"] = self.randomBoolean()
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = randint(6, 9)
        data["first_sit"] = randint(6, 9)
        data["first_walk"] = randint(9, 14)
        data["first_words"] = randint(11, 15)
        data["birth_weight"] = 3
        data["birth_weight_metric"] = self.randomBoolean()
        data["height"] = 61
        data["height_metric"] = self.randomBoolean()
        data["weight"] = 9
        data["weight_metric"] = self.randomBoolean()

        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to set medical history clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))

    def genFLast(self):
        names = ["Gomez", "Sanchez", "Romero", "Gutierrez", "Lopez"];
        return names[randint(0, len(names) - 1)]

    def genMLast(self):
        names = ["Gomez", "Sanchez", "Romero", "Gutierrez", "Lopez"];
        return names[randint(0, len(names) - 1)]

    def genFirst(self, male):
        maleNames = ["Roberto", "Angel", "Jose", "Luis"];
        femaleNames = ["Yolanda", "Gloria", "Maria", "Alicia"];
        if male:
            return maleNames[randint(0, len(maleNames) - 1)]
        else:
            return femaleNames[randint(0, len(femaleNames) - 1)]

    def genMiddle(self, male):
        maleNames = ["Roberto", "Angel", "Jose", "Luis"];
        femaleNames = ["Yolanda", "Gloria", "Maria", "Alicia"];
        if male:
            return maleNames[randint(0, len(maleNames) - 1)]
        else:
            return femaleNames[randint(0, len(femaleNames) - 1)]


    def createAllPatients(self, clinic, count, doImages, doXRay):
        for i in xrange(0, count):
            data = {}
            male = randint(0, 1)
            data["paternal_last"] = "{}{}".format(i, self.genFLast())
            data["maternal_last"] = "{}".format(self.genMLast())
            data["first"] = "{}".format(self.genFirst(male))
            data["middle"] = "{}".format(self.genMiddle(male))
            data["suffix"] = "Jr."
            data["prefix"] = ""
            data["dob"] = "{}/{}/200{}".format(randint(1,12), randint(1,30), randint(0, 9))
            if male:
                data["gender"] = "Male"
            else:
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
            id = self.createPatient(data)
            self.createMedicalHistory(clinic, id)
            if doXRay:
                if self.randomBoolean() == True:
                    self.createXRay(clinic, id)
 
            if doImages:
                self.addPhoto(clinic, data["gender"], id)

    def createClinicResourcesFromFile(self, path):
        f = open(path, 'r')
        x = f.read()
        x = json.loads(x)
        f.close()
        self.createCategories(x["categories"])
        clinic = self.createClinic(x["name"], int(x["duration"]))
        for y in x["stations"]:
            station = self.createStation(y["name"], y["level"])
            if y["name"] == "X-Ray":
                self._xray = station
            elif y["name"] == "Audiology":
                self._audiology = station
            elif y["name"] == "Speech":
                self._speech = station
            elif y["name"] == "Dental":
                self._dental = station
            elif y["name"] == "Ortho":
                self._ortho = station
            elif y["name"] == "ENT":
                self._ent = station
            elif y["name"] == "Surgery Screening":
                self._surgery = station
            for z in y["stations"]:
                self.createClinicStation(clinic, station, (z["name"], z["name_es"]))
    
    def getXray(self):
        return self._xray

    def getDental(self):
        return self._dental

    def getENT(self):
        return self._ent

    def getAudiology(self):
        return self._audiology

    def getOrtho(self):
        return self._ortho

    def getSurgery(self):
        return self._surgery

    def createClinicResources(self):
        print("Creating patient categories")
        self.createCategories()
        print("Creating clinic")
        clinic = self.createClinic("Ensenada", 1)
        print("Creating stations")
        self._dental = self.createStation("Dental", 1)
        self._ent = self.createStation("ENT", 2)
        self._ortho = self.createStation("Ortho", 1) 
        self._xray = self.createStation("X-Ray", 2) 
        self._surgery = self.createStation("Surgery Screening", 1) 
        self._speech = self.createStation("Speech", 1) 
        self._audiology = self.createStation("Audiology", 1) 

        dentalStations = []
        for x in [("Dental1","Dental1"), ("Dental2","Dental2"), ("Dental3", "Dental3"), ("Dental4","Dental4"), ("Dental5","Dental5")]:
            print("Creating station {}".format(x))
            dentalStations.append(self.createClinicStation(clinic, self._dental, x))
        entStation = self.createClinicStation(clinic, ent, ("ENT","Otorrino")) 
        print("Creating station {}".format("ENT"))
        orthoStations = []
        for x in [("Ortho1","Orto1"), ("Ortho2","Orto2")]:
            print("Creating station {}".format(x))
            orthoStations.append(self.createClinicStation(clinic, ortho, x))
        print("Creating station {}".format("X-Ray"))
        xrayStation = self.createClinicStation(clinic, self._xray, ("X-Ray","Rayos X")) 
        print("Creating station {}".format("Surgery Screening"))
        surgeryStation = self.createClinicStation(clinic, surgery, ("Surgery Screening","Cirugía")) 
        print("Creating station {}".format("Speech"))
        speechStation = self.createClinicStation(clinic, speech, ("Speech","Terapia Del Habla")) 
        print("Creating station {}".format("Audiology"))
        audiologyStation = self.createClinicStation(clinic, audiology, ("Audiology", "Audiología")) 

def usage():
    print("mockclinic [-h host] [-p port] [-u username] [-w password] [-y] [-i] [-q] [-r] [-c] [-f filename] [-a] [-x] [-n limit]") 
    print("-y -- create a random number of simulated patients") 
    print("-n -- limit number of simulated patients to specified value") 
    print("-i -- randomly create simulated headshots") 
    print("-q -- generate return to clinics randomly") 
    print("-r -- simulate registering all patients") 
    print("-c -- simulate checking patients in") 
    print("-f -- read clinic description from file") 
    print("-a -- simulate stations going away") 
    print("-x -- randomly generate return to clinic station") 
    print("-l -- randomly generate xray") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "lqrcyaixh:p:u:w:f:n:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    host = "127.0.0.1"
    port = 8000
    clinicFile = ""
    username = None
    password = None
    doCheckins = False
    doPatients = False
    doRegister = False
    doAway = False
    doImages = False
    doXRay = False
    fromFile = False
    doReturnToClinic = False
    doReturnToClinicStation = False
    numAway = 0
    limit = 130
    for o, a in opts:
        if o == "-a":
            doAway = True
        elif o == "-i":
            doImages = True
        elif o == "-c":
            doCheckins = True
        elif o == "-f":
            fromFile = True
            clinicFile = a
        elif o == "-r":
            doRegister = True
        elif o == "-y":
            doPatients = True
        elif o == "-l":
            doXRay = True
        elif o == "-q":
            doReturnToClinic = True
        elif o == "-x":
            doReturnToClinicStation = True
        elif o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-n":
            limit = int(a)
        else:   
            assert False, "unhandled option"

    if doReturnToClinicStation == True and doCheckins == False:
        print("warning: -x selected but not -c. Adding -c since checkins are required to exercise return to clinicstation functionality")
        doCheckins = True

    mock = MockClinic(host, port, username, password)   
    mock.simulateReturnToClinicStation(doReturnToClinicStation)
    if mock.login():
        if fromFile:
            mock.createClinicResourcesFromFile(clinicFile)
        else:
            mock.createClinicResources()
        clinic = mock.getClinic()
        if doPatients:
            print("Sleeping for 20 seconds, please wait.")
            time.sleep(20)
            lowerLimit = limit - 10;
            if lowerLimit < 0:
                lowerLimit = 0;
            n = randint(lowerLimit, limit)
            print("Registering {} patients for this clinic".format(n))
            mock.createAllPatients(clinic, n, doImages, doXRay)
        checkinThreads = None
        awayThreads = None
        if doCheckins:
            checkinThreads = mock.simulateCheckins()
        if doAway:
            awayThreads = mock.simulateAway() 
        # NOTYET
        #if doReturnToClinicStation:
        #    mock.processReturnToClinicStationStateChanges() 
        if doReturnToClinic:
            stations = mock.getStations()
            intervals = [3, 6, 9, 12]
            for x in mock.getPatients():
                interval = intervals[randint(0, len(intervals) - 1)]
                stationid = stations[randint(0, len(stations) - 1)]
                mock.createReturnToClinic( x, clinic, stationid, interval)
        if doRegister:
            for x in mock.getPatients():
                time.sleep(randint(1, 30))
                cat = mock.getRandomCategory()
                mock.createRegistration(clinic, x)
                routingslip = mock.createRoutingSlip(x, clinic, cat)
                print("\n\nCreating routingslip for {} patient {} at time {}".format(cat, x, datetime.now().strftime("%H:%M:%S")))
                if cat == "Dental":
                    xray = mock.getXray()
                    dental = mock.getDental()
                    print("Adding xray")
                    mock.createRoutingSlipEntry(routingslip, xray)    
                    print("Adding dental")
                    mock.createRoutingSlipEntry(routingslip, dental)    
                elif cat == "New Cleft" or cat == "Returning Cleft":
                    st = mock.getENT()
                    print("Adding ENT")
                    mock.createRoutingSlipEntry(routingslip, st) 
                    st = mock.getSurgery()
                    print("Adding Surgery Screening")
                    mock.createRoutingSlipEntry(routingslip, st) 
                elif cat == "Ortho":
                    ortho = mock.getOrtho()
                    print("Adding Ortho")
                    mock.createRoutingSlipEntry(routingslip, ortho) 
                elif cat == "Hearing Aids":
                    audiology = mock.getAudiology()
                    print("Adding Audiology")
                    mock.createRoutingSlipEntry(routingslip, audiology) 
                elif cat == "Ears":
                    ent = mock.getENT()
                    print("Adding ENT")
                    mock.createRoutingSlipEntry(routingslip, ent) 
                elif cat == "Ortho":
                    ortho = mock.getOrtho()
                    print("Adding Ortho")
                    mock.createRoutingSlipEntry(routingslip, ent) 
                else:
                    print("Adding Random Stations")
                    for y in mock.getStations():
                        if randint(0, 1) == 1:
                            print("Adding station {} to routing slip".format(mock.getStationName(y)))
                            mock.createRoutingSlipEntry(routingslip, y)    
        mock.logout()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

if __name__ == "__main__":
    main()
