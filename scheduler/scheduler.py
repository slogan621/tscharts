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
import getopt, os, sys, time
import json
import datetime 

# unit tests provide a set of good utilities for accessing the web services.

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.routingslip.routingslip import GetRoutingSlip, GetRoutingSlipEntry, UpdateRoutingSlipEntry
from test.clinic.clinic import GetClinic, GetAllClinics
from test.clinicstation.clinicstation import GetClinicStation

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tscharts.settings")
import django
django.setup()

from queue.models import QueueStatus, Queue, QueueEntry
from routingslip.models import RoutingSlipEntry
from patient.models import Patient
from clinic.models import Clinic
from station.models import Station
from clinicstation.models import ClinicStation 

class ClinicStationQueueEntry():
    def __init__(self):
        self._patientid = None
        self._timein = datetime.datetime.utcnow()
        self._elapsedtime = 0
        self._timeout = 0
        self._queueid = None
        self._routingslipentryid = None

    def setQueue(self, id):
        self._queueid = id

    def setRoutingSlipEntry(self, id):
        self._routingslipentryid = id

    def setPatientId(self, id):
        self._patientid = id

    def getElapsedTime(self):
        return self._elapsedtime

    def update(self):
        ret = False
        self._elapsedtime = datetime.datetime.utcnow() - self._timein
        q = None
        try:
            q = QueueEntry.objects.get(queue=self._queueid,
                                       patient=self._patientid)
        except:
            q = None
            
        if (q != None) :
            q.waittime = str(self._elapsedtime)
            q.estwaittime = q.waittime  # XXX
            q.save()            
            ret = True
        else:
            print("unable to get queue entry queue {} patient {} routingslipentry {}".format(self._queueid, self._patientid, self._routingslipentryid))
        return ret

    def __str__(self):
        self._elapsedtime = datetime.datetime.utcnow() - self._timein
        return "id: {} time in: {} waiting time {}".format(self._patientid, self._timein.strftime("%H:%M:%S"), self._elapsedtime)

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
        self._dbQueues = {}
        self._dbQueueEntries = {}
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

    def __del__(self):
        logout = Logout(self._host, self._port)
        ret = logout.send(timeout=30)

    def getClinicStationName(self, id):
        ret = None
        for x in self._clinicstations:
            if x["id"] == id:
                ret = x["name"]
                break
        return ret 

    def createDbQueue(self, clinicid, stationid, clinicstationid):
        queue = None

        try:
            aClinic = Clinic.objects.get(id=clinicid)
        except:
            print("createDbQueue unable to get clinic {}".format(clinicid))
        try:
            aStation = Station.objects.get(id=stationid)
        except:
            print("createDbQueue unable to get station {}".format(stationid))
        try:
            aClinicStation = ClinicStation.objects.get(id=clinicstationid)
        except:
            print("createDbQueue unable to get clinicstation {}".format(clinicstationid))

        try:
            queue = Queue(clinic = aClinic,
                          station = aStation,
                          clinicstation = aClinicStation,
                          avgservicetime = datetime.time(0,0))
            queue.save()
        except:
            print("createDbQueue unable to create queue")
        return queue

    def createDbQueueEntry(self, queueid, patientid, routingslipentryid):
        queueent = None

        try:
            aQueue = Queue.objects.get(id=queueid)
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("createDbQueueEntry unable to get queue {}".format(queueid))
        try:
            aPatient = Patient.objects.get(id=int(patientid))
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("createDbQueueEntry unable to get patient {}".format(patientid))
        try:
            aRoutingSlipEntry = RoutingSlipEntry.objects.get(id=int(routingslipentryid))
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("createDbQueueEntry unable to get routingslipentry {}".format(routingslipentryid))

        try:
            queueent = QueueEntry(queue = aQueue,
                                  patient = aPatient,
                                  timein = datetime.datetime.utcnow(),
                                  routingslipentry = aRoutingSlipEntry)
            queueent.save()
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("createDbQueueEntry unable to create queue entry")
        return queueent

    def updateClinicStations(self):
        self._clinicstations = self.getClinicStations()
        
        for x in self._clinicstations:
            idstring = str(x["id"])
            if not idstring in self._queues:
                self._dbQueues[idstring] = self.createDbQueue(x["clinic"], x["station"], x["id"]) 
                self._queues[idstring] = [] 
            if not str(x["station"]) in self._stationToClinicStationMap:
                self._stationToClinicStationMap[str(x["station"])] = []
            if not x["id"] in self._stationToClinicStationMap[str(x["station"])]:
                self._stationToClinicStationMap[str(x["station"])].append(x["id"])

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
            today = datetime.datetime.utcnow()
            x = GetAllClinics(self._host, self._port, self._token) 
            ret = x.send(timeout=30)
            if ret[0] == 200:
                for x in ret[1]:
                    start = datetime.datetime.strptime(x["start"], "%m/%d/%Y")
                    end = datetime.datetime.strptime(x["end"], "%m/%d/%Y")
                    if today >= start and today <= end:
                        retval = x
                        self._clinicid = x["id"]
                        self._clinic = x
                        break
        return retval

    def getClinicStationsForStation(self, stationid):
        return self._stationToClinicStationMap[str(stationid)]

    def dumpQueues(self):
        #os.system("clear")
        minQ = 9999
        maxQ = -9999 
        minWait = datetime.timedelta(days=999)
        maxWait = datetime.timedelta(seconds=0)
        total = 0
        numQueues = 0
        totalWait = datetime.timedelta(seconds=0)
        print("\nClinic queue report UTC time {}\n".format(datetime.datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")))
        for k, v in self._queues.iteritems():
            print("***** Station {} *****".format(self.getClinicStationName(int(k))))
            if len(v):
                localWait = datetime.timedelta(seconds=0)
                numQueues = numQueues + 1
                print("{} patients waiting".format(len(v)))
                total += len(v)
                if len(v) < minQ:
                    minQ = len(v)
                if len(v) > maxQ:       
                    maxQ = len(v)
                for x in v:
                    print("    {}".format(str(x["qent"])))
                    wait = x["qent"].getElapsedTime()
                    localWait += wait
                    if wait < minWait:
                        minWait = wait
                    if wait > maxWait:
                        maxWait = wait
                    totalWait = totalWait + wait
                print("avg wait: {}".format(localWait/len(v)))
            else:
                print("    No entries")
        if numQueues > 0 and total > 0:
            avg = total / numQueues
            avgWait = totalWait / total
            qs = QueueStatus()
            qs.numwaiting = total
            qs.minq = minQ
            qs.maxq = maxQ
            qs.avgq = avg
            qs.minwait = str(minWait)
            qs.maxwait = str(maxWait)
            qs.avgwait = str(avgWait)
            qs.clinic_id = self._clinicid
            try:
                qsold = QueueStatus.objects.filter()
                if qsold:
                    for x in qsold:
                        x.delete()
            except:
                pass
            qs.save()
            print("\nNumber of patients waiting {} smallest Q {} largest Q {} avg Q {} smallest wait {} largest wait {} avg wait {}".format(total, minQ, maxQ, avg, minWait, maxWait, avgWait))

    def getClinicStations(self):
        retval = []
        clinic = self.getClinic()

        if clinic:
            x = GetClinicStation(self._host, self._port, self._token)
            x.setClinic(clinic["id"])
            ret = x.send(timeout=30)
            if ret[0] == 200:
                retval = ret[1]
                #print retval
        return retval

    def addToQueue(self, entry, patientid):
        min = 9999      
        index = None
        clinicstations = self.getClinicStationsForStation(entry["station"])
        for x in clinicstations:
            tmp = len(self._queues[str(x)])
            if tmp < min:
                min = tmp
                index = str(x) 
        if not entry in self._queues[index]:
            qent = ClinicStationQueueEntry()
            qent.setRoutingSlipEntry(entry["id"])
            qent.setPatientId(patientid)
            qent.setQueue(index)
            entry["qent"] = qent
            self._queues[index].append(entry)
            dbQueue = self._dbQueues[index]
            # create queue entry
            dbQueueEntry = self.createDbQueueEntry(dbQueue.id,
                                                   patientid, 
                                                   entry["id"])
            if dbQueueEntry:
                self._dbQueueEntries[index] = dbQueueEntry

    def sortQueueablesByPriority(self, queueables):
        tmp = sorted(queueables, key=lambda k: k["order"])
        ret = []

        # create a list of the highest priority item
        highest = -99999
        for x in tmp:
            if x["order"] >= highest:
                ret.append(x)
                highest = x["order"]
            else:
                break
        return ret

    def getSmallestLengthQueue(self, queueables):
        ret = None
        smallest = 9999

        for x in queueables:
            clinicstations = self.getClinicStationsForStation(x["station"])
            for clinicstation in clinicstations:
                tmp = len(self._queues[str(clinicstation)])
                if tmp < smallest:
                    ret = x
                    smallest = tmp
        return ret

    def isWaiting(self, routing):
        retval = False

        for x in routing:
            entry = GetRoutingSlipEntry(self._host, self._port, self._token, x)
            ret = entry.send(timeout=30)
            if ret[0] == 200:
                state = ret[1]["state"] 

                if state == "Scheduled":
                    retval = True
                    break

        return retval

    def findQueueableEntry(self, routing):
        queueables = []
        retval = None      # default: nothing to queue on this routing slip

        if not self.isWaiting(routing):
            for x in routing:
                entry = GetRoutingSlipEntry(self._host, self._port, self._token, x)
                ret = entry.send(timeout=30)
                if ret[0] == 200:
                    state = ret[1]["state"] 

                    if state == "New":
                        queueables.append(ret[1])

        if len(queueables):

            # found something to schedule, find highest priority with smallest queue size

            if len(queueables) == 1:
                retval = queueables[0]          # last station for this patient, choose it
            else:       
                # sort the queueables into stations in order of highest priority to lowest.

                tmp = self.sortQueueablesByPriority(queueables)

                retval = self.getSmallestLengthQueue(tmp) 
                
        return retval

    def markScheduled(self, entry):
        x = UpdateRoutingSlipEntry(self._host, self._port, self._token, entry["id"])
        x.setState("Scheduled")
        ret = x.send(timeout=30)

    def run(self):

        while True:
            clinic = self.getClinic()
            if not clinic:
                continue

            self.updateClinicStations()
            self.dumpQueues()

            # get all the routing slips for the clinic

            x = GetRoutingSlip(self._host, self._port, self._token)
            x.setClinic(clinic["id"])
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
                        self.addToQueue(entry, i["patient"])
                        break

            for k, v in self._queues.iteritems():
                for y in v:
                    ret = y["qent"].update()
                    if not ret:
                        v.remove(y)

            time.sleep(5)

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
