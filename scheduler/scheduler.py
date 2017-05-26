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

import daemon
import getopt, sys, time
import json
from datetime import datetime

# unit tests provide a set of good utilities for accessing the web services.

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.routingslip.routingslip import GetRoutingSlip, GetRoutingSlipEntry
from test.clinic.clinic import GetClinic, GetAllClinics
from test.clinicstation.clinicstation import GetClinicStation

class ClinicStationQueueEntry():
    def __init__(self):
        self._patientid = None

    def setPatient(self, id):
        self._patientid = id

class Scheduler():
    def __init__(self, host, port, username, password, clinicid=None):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._clinicid = clinicid
        self._clinic = None
        self._clinicstations = []
        self._queues = {} 
        self._stationToClinicStationMap = {}
        fail = False
        try:
            login = Login(self._host, self._port, self._username, self._password)
            ret = login.send(timeout=30)
            if ret[0] == 200:
                self._token = ret[1]["token"]
            else:
                fail = True
        except:
            fail = True

        if fail:
            print("failed to login")
            sys.exit(2)

        self._clinicstations = self.getClinicStations()
        
        for x in self._clinicstations:
            self._queues[str(x["id"])] = [] 
            self._stationToClinicStationMap[str(x["station"])]=x["id"]

    def __del__(self):
        logout = Logout(self._host, self._port)
        ret = logout.send(timeout=30)

    def getClinic(self):
        retval = None

        if self._clinic:
            retval = self._clinic
        elif self._clinicid:
            x = GetClinic(self._host, self._port, self._token, self._clinicid)
            ret = x.send(timeout=30)
            if ret[0] == 200:
                retval = ret[1]

        if not retval:
            today = datetime.utcnow()
            x = GetAllClinics(self._host, self._port, self._token) 
            ret = x.send(timeout=30)
            if ret[0] == 200:
                for x in ret[1]:
                    start = datetime.strptime(x["start"], "%m/%d/%Y")
                    end = datetime.strptime(x["end"], "%m/%d/%Y")
                    if today >= start and today <= end:
                        retval = x
                        break
        return retval

    def getClinicStationForStation(stationid):
        return self.stationToClinicStationMap[str(stationid)]

    def getClinicStations(self):
        retval = []
        clinic = self.getClinic()

        if clinic:
            x = GetClinicStation(self._host, self._port, self._token)
            x.setClinic(clinic["id"])
            ret = x.send(timeout=30)
            if ret[0] == 200:
                retval = ret[1]
        return retval

    def addToQueue(self, entry):
        clinicstation = getClinicStationForStation(entry["station"])
        self._queues[str(clinicstation)].append(entry)

    def findQueueableEntry(self, routing):
        retval = None      # default: nothing to queue on this routing slip
        for x in routing:
            entry = GetRoutingSlipEntry(self._host, self._port, self._token, x)
            ret = entry.send(timeout=30)
            if ret[0] == 200:
                state = ret[1]["state"] 
                # if currently scheduled, then nothing to do for this patient

                if state == "Scheduled":
                    retval = None
                    break

                if state == "New":
                    # if this entry is the first or the hightest priority
                    # seen so far, then select it
                    if not retval:
                        retval = ret[1]    # first seen for patient
                    elif ret[1]["order"] > retval["order"]:
                        retval = ret[1]    # highest priority
        return retval

    def markScheduled(self, entry):
        x = UpdateRoutingSlipEntry(self._host, self._port, self._token, entry["id"])
        x.setState("Scheduled")
        ret = x.send(timeout=30)

    def run(self):
        if not self._clinicid:
            return

        while True:
            time.sleep(30)

            # get all the routing slips for the clinic

            x = GetRoutingSlip(self._host, self._port, self._token)
            x.setClinic(self._clinicid)
            ret = x.send(timeout=30)
            if ret[0] == 200:
                results = ret[1]

                # process each of the routing slips

                for i in results:
                    routing = i["routing"]
                    entry = self.findQueueableEntry(routing)
                    if entry:
                        # update the routingslip entry state to "Scheduled"
                        self.markScheduled(entry)
                        # append the entry to the corresponding
                        # clinicstation queue
                        self.addToQueue(entry)

def usage():
    print("scheduler [-c clinicid] [-h host] [-p port] [-u username] [-w password]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:h:p:u:w:")
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    host = "127.0.0.1"
    port = 8000
    username = None
    password = None
    clinicid = None
    for o, a in opts:
        if o == "-c":
            clinicid = a
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
    #with daemon.DaemonContext():
    x = Scheduler(host, port, username, password, clinicid)
    x.run()

if __name__ == '__main__':
    main() 
