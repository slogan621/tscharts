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

from statechange.models import StateChange
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
        self._routingslip = None

    def setQueue(self, id):
        self._queueid = id

    def setRoutingSlip(self, id):
        self._routingslip = id

    def getRoutingSlip(self):
        return self._routingslip

    def setRoutingSlipEntry(self, id):
        self._routingslipentryid = id

    def getRoutingSlipEntry(self):
        return self._routingslipentryid

    def setPatientId(self, id):
        self._patientid = id

    def getPatientId(self):
        return self._patientid

    def getElapsedTime(self):
        return self._elapsedtime

    def getEstWaitTime(self, queueentryid):   
        # use self._queueid to determine relative position of
        # queueentry and the avgservice time, plus the time the
        # current patient (if any) has been in service, and then
        # compute an estimated time for this particular entry
        return self._elapsedtime  # XXX

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
            q.waittime = str(self.getElapsedTime())
            q.estwaittime = str(self.getEstWaitTime(q.id))
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
        self._clinicStationToStationMap = {}
        self._clinicStationActiveMap = {}
        self._clinicStationAwayMap = {}
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

        create = False
        try:
            queue = Queue.objects.filter(clinic=aClinic, station=aStation,
                                         clinicstation=aClinicStation);
            if queue and len(queue) > 0:
                queue = queue[0]
            else:
                create = True
        except:
            create = True

        if create == True:
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

    def deleteDbQueueEntry(self, queueid, patientid, routingslipentryid):
        queueent = None
        ret = False

        try:
            aQueue = Queue.objects.get(id=queueid)
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("deleteDbQueueEntry unable to get queue {}".format(queueid))
        try:
            aPatient = Patient.objects.get(id=int(patientid))
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("deleteDbQueueEntry unable to get patient {}".format(patientid))
        try:
            aRoutingSlipEntry = RoutingSlipEntry.objects.get(id=int(routingslipentryid))
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("deleteDbQueueEntry unable to get routingslipentry {}".format(routingslipentryid))

        try:
            queueent = QueueEntry.objects.get(queue = aQueue,
                                  patient = aPatient,
                                  routingslipentry = aRoutingSlipEntry)
            if queueent:
                queueent.delete()
                ret = True
        except:
            print("exception: {}".format(sys.exc_info()[0]))
            print("deleteDbQueueEntry unable to delete queue entry queue ({}) {} patient ({}) {} routingslipentry ({}) {}".format(queueid, aQueue, patientid, aPatient, routingslipentryid, aRoutingSlipEntry))
        return ret

    def getClinicStationAvgServiceTime(self, statechanges):
        sumt = 0
        count = 0
        if len(statechanges) == 0:
            return "00:00:00"
        for x in statechanges:
            if x.state == 'i':
                t0 = x.time
            else:
                t1 = x.time
                delta = t1 - t0
                sumt += delta.total_seconds()
                count = count + 1
        if count == 0:
            return "00:00:00"
        hours = 0
        minutes = 0
        seconds = 0
        avg_secs = int(sumt / count)

        hours = avg_secs / 3600
        minutes = (avg_secs - (hours * 3600)) / 60
        seconds = avg_secs - ((hours * 3600) + (minutes * 60))    
        strtime = "{}:{}:{}".format(hours, minutes, seconds)
        ret = datetime.datetime.strptime(strtime, '%H:%M:%S').time()
        return ret

    def verifyStateChanges(self, statechanges):
        ret = True

        count = 0
        for x in statechanges:          
            if count % 2 == 0:
                if not x.state == 'i':
                    print("statechanges expected in 'i' but got '{}'".format(x.state))
                    ret = False
                    break
            else:
               if not x.state == 'o':
                   print("statechanges expected out 'o' but got '{}'".format(x.state))
                   ret = False
                   break
            count = count + 1
        return ret

    def updateQueueAvgServiceTime(self):
        for x in self._clinicstations:
            # get statechange sorted by date for this clinicstation. Order
            # should be in, out pairs for each patient that has visited the
            # clinic. Verify this, and sum the time deltas between arriving 
            # and leaving. Finally, compute average of these time deltas.

            try:
                aClinicStation = ClinicStation.objects.get(id=x["id"])
                if not aClinicStation:
                    print("updateQueueAvgServiceTime not found clinicstation {}".format(x["id"]))
                    
            except:
                print("updateQueueAvgServiceTime unable to get clinicstation {}".format(x["id"]))
                continue
            try:
                statechanges = StateChange.objects.filter(clinicstation=aClinicStation).order_by("time")              
            except:
                print("updateQueueAvgServiceTime unable to get statechanges {}".format(x["id"]))
                continue
            if statechanges and len(statechanges):
                if not self.verifyStateChanges(statechanges): 
                    print("updateQueueAvgServiceTime statechanges for clinicstation {} are not valid".format(x))                        
                    continue
                avg = self.getClinicStationAvgServiceTime(statechanges)
                try:
                    aQueue = Queue.objects.filter(clinicstation=aClinicStation)
                    if aQueue and len(aQueue) == 1:
                        aQueue[0].avgservicetime = avg
                        aQueue[0].save() 
                except:
                    print("exception: {}".format(sys.exc_info()[0]))
                    print("updateQueueAvgServiceTime unable to get queue")

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
            self._clinicStationToStationMap[str(x["id"])] = str(x["station"])
            self._clinicStationActiveMap[str(x["id"])] = x["active"]
            self._clinicStationAwayMap[str(x["id"])] = x["away"]

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

    def getEmptyQueues(self):
        ret = []
        for k, v in self._queues.iteritems():
            active = self._clinicStationActiveMap[str(k)]
            away = self._clinicStationAwayMap[str(k)]
            if away == False and active == False and not len(v):
                ret.append(k)
        return ret

    def fillAnEmptyQueue(self):
        empty = self.getEmptyQueues()
        for x in empty:
            station = self._clinicStationToStationMap[str(x)]
            for k, v in self._queues.iteritems():
                active = self._clinicStationActiveMap[str(k)]
                away = self._clinicStationAwayMap[str(k)]
                if k == x:
                    if len(v):
                        break    # queue is no longer empty, go to next queue
                    else:
                        continue # queue is one we are trying to fill, skip
                if len(v) == 1 and active == False and away == False:
                    continue     # patient is probably being retrieved, don't move from this queue
                '''
                iterate the queue, looking for a patient that has the 
                station of the empty queue in his or her routing slip. 
                If found, move that patient to the queue that is empty.
                ''' 
                count = 0 
                for item in v:
                    if active == False:
                        count = count + 1  # if not active, skip first in list
                        continue
                    qent = item["qent"] 
                    r = GetRoutingSlip(self._host, self._port, self._token)
		    r.setId(qent.getRoutingSlip())
                    ret = r.send(timeout=30)
                    if ret[0] == 200:
                        routing = ret[1]["routing"]
                        patient = ret[1]["patient"]
                        for y in routing:
                            entry = GetRoutingSlipEntry(self._host, self._port, self._token)
			    entry.setId(y)
                            ret = entry.send(timeout=30)
                            if ret[0] == 200:
                                rse = ret[1]
                                state = ret[1]["state"] 
                                if str(ret[1]["station"]) == station and (state == "Scheduled"):
                                    print ("************ moving a queue item ******************* item {} patient {}".format(y, patient))

                                    dbQueue = self._dbQueues[k]
                                    ret = self.deleteDbQueueEntry(dbQueue.id, qent.getPatientId(), rse["id"])
                                    if ret == True:
                                        self.markNew(rse)
                                        self._queues[k].remove(item)

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
        else:
            avg = 0
            avgWait = "00:00"
            minWait = "00:00"
            maxWait = "00:00"

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
        return retval

    def addToQueue(self, routingslipentry, patientid):
        ret = False
        min = 9999      
        index = None
        clinicstations = self.getClinicStationsForStation(routingslipentry["station"])
        for x in clinicstations:
            away = self._clinicStationAwayMap[str(x)]
            if away == True:
                continue
            tmp = len(self._queues[str(x)])
            if self._clinicStationActiveMap[str(x)] == True:
                tmp += 1
            if tmp < min:
                min = tmp
                index = str(x) 
        if index:
            isInQueue = routingslipentry in self._queues[index]
            if index and (not isInQueue):
                qent = ClinicStationQueueEntry()
                qent.setRoutingSlip(routingslipentry["routingslip"])
                qent.setRoutingSlipEntry(routingslipentry["id"])
                qent.setPatientId(patientid)
                qent.setQueue(index)
                routingslipentry["qent"] = qent
                self._queues[index].append(routingslipentry)
                dbQueue = self._dbQueues[index]
                # create queue entry
                dbQueueEntry = self.createDbQueueEntry(dbQueue.id,
                                                       patientid, 
                                                       routingslipentry["id"])
                if dbQueueEntry:
                    self._dbQueueEntries[index] = dbQueueEntry
                ret = True
        return ret

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
                # don't schedule into away queues
                away = self._clinicStationAwayMap[str(clinicstation)]
                if away == True:
                    continue
                tmp = len(self._queues[str(clinicstation)])
                if tmp < smallest:
                    ret = x
                    smallest = tmp
        return ret

    def isWaiting(self, routing):
        retval = False

        for x in routing:
            entry = GetRoutingSlipEntry(self._host, self._port, self._token)
	    entry.setId(x)
            ret = entry.send(timeout=30)
            if ret[0] == 200:
                state = ret[1]["state"] 

                if state == "Scheduled" or state == "Checked In":
                    retval = True
                    break

        return retval

    def findQueueableEntry(self, routing):
        queueables = []
        retval = None      # default: nothing to queue on this routing slip

        if not self.isWaiting(routing):
            for x in routing:
                entry = GetRoutingSlipEntry(self._host, self._port, self._token)
	    	entry.setId(x)
                ret = entry.send(timeout=30)
                if ret[0] == 200:
                    state = ret[1]["state"] 
                    if state == "New" :
                        queueables.append(ret[1])
                else:
                    print("findQueueableEntry failure in GetRoutingSlipEntry".format(ret[0]))

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
        if ret[0] != 200:
            print("markScheduled failure for entry {}".format(entry["id"]))

    def markNew(self, entry):
        x = UpdateRoutingSlipEntry(self._host, self._port, self._token, entry["id"])
        x.setState("New")
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("markNew failure for entry {}".format(entry["id"]))

    def run(self):

        while True:
            clinic = self.getClinic()
            if not clinic:
                continue

            self.updateClinicStations()

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
                        # append the entry to the corresponding
                        # clinicstation queue
                        if self.addToQueue(entry, i["patient"]) == True:
                            # update the routingslip entry state to "Scheduled"
                            self.markScheduled(entry)
                            break
                        else:
                            print("Unable to add item to queue");

            else:
                print("GetRoutingSlip failed"); 
            for k, v in self._queues.iteritems():
                for y in v:
                    ret = y["qent"].update()
                    if not ret:
                        v.remove(y)

            self.dumpQueues()
            self.fillAnEmptyQueue()
            self.updateQueueAvgServiceTime()
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
