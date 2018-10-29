#(C) Copyright Syd Logan 2018
#(C) Copyright Thousand Smiles Foundation 2018
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

import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]

class UpdateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateClinicStation, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

    def setAway(self, away):
        self._payload["away"] = away
        self.setPayload(self._payload)

    def setFinished(self, finished):
        self._payload["finished"] = finished
        self.setPayload(self._payload)

    def setActive(self, active):
        self._payload["active"] = active
        self.setPayload(self._payload)

    def setName(self, name):
        self._payload["name"] = name
        self.setPayload(self._payload)

    def setNameES(self, name):
        self._payload["name_es"] = name
        self.setPayload(self._payload)

    def setLevel(self, level):
        self._payload["level"] = level
        self.setPayload(self._payload)

    def setActivePatient(self, patient):
        self._payload["activepatient"] = patient
        self.setPayload(self._payload)

    def setNextPatient(self, patient):
        self._payload["nextpatient"] = patient
        self.setPayload(self._payload)

    def setAwayTime(self, minutes):
        self._payload["awaytime"] = minutes
        self.setPayload(self._payload)

def updateClinicStation(id, awayTime, nextPatient, activePatient, level, away, finished, active, name, spanishName):
    count = 0
    if finished == True:
        count += 1 
    if active == True:
        count += 1
    if away  == True:
        count += 1

    if count >= 2:
        print("Only one of away, finished, or active state can be set")
        usage()
        sys.exit(1)

    x = UpdateClinicStation(host, port, token, id)
    if awayTime != None:
        x.setAwayTime(awayTime)
    if nextPatient != None:
        x.setNextPatient(nextPatient)
    if activePatient != None:
        x.setActivePatient(activePatient)
    if level != None:
        x.setLevel(level)
    if away != None:
        x.setAway(away)
    if finished != None:
        x.setFinished(finished)
    if active != None:
        x.setActive(active)
    if name != None:
        x.setName(name)
    if spanishName != None:
        x.setnameES(spanishName)
            
    ret = x.send(timeout=30)
    if ret[0] == 200:
        print("Successfully updated clinic station {}".format(id))
    else:
        print("Error updating clinic station {}: {}".format(id, ret[0]))

def usage():
    print("updateclinicstation [-h host] [-p port] [-u username] [-w password] [-i id] [-t awaytime_in_min] [-z nextpatient] [-c activepatient] [-l level] [-b] [-f] [-a] [-n name] [-s spanish_name]")
    print("-b puts station in away state")
    print("-f puts station in finished state")
    print("-a puts station in active state")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:i:t:z:c:l:bfan:s:")
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
    id = None
    awayTime=None
    nextPatient=None
    activePatient=None
    level=None
    away=None
    finished=None
    active=None
    name=None
    spanishName=None 
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-i":
            id = int(a)
        elif o == "-t":
            awayTime = int(a)
        elif o == "-z":
            nextPatient = int(a)
        elif o == "-c":
            activePatient = int(a)
        elif o == "-l":
            level = int(a)
        elif o == "-b":
            away = True
        elif o == "-f":
            finished = True
        elif o == "-a":
            active = True
        elif o == "-n":
            name = a
        elif o == "-s":
            spanishName = a
        else:
            assert False, "unhandled option"
    setUp()
    updateClinicStation(id, awayTime, nextPatient, activePatient, level, away, finished, active, name, spanishName)
if __name__ == "__main__":
    main()

