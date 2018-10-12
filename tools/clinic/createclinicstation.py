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

import unittest
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

class CreateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, clinic, station, name, name_es, level):
        super(CreateClinicStation, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        active = False
        finished = False
        away = False

        payload = {"clinic": clinic, "away": away, "station": station, "active": active, "name": name, "finished": finished, "name_es": name_es, "level": level}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/")

def createClinicStation(clinic, station, name, spanishName, level):
    x = CreateClinicStation(host, port, token, clinic, station, name, spanishName, level)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        print("created clinicstation {} {} with id {}".format(name, spanishName, ret[1]["id"]))
    else:
        print("failed to create clinicstation {} {}".format(name, spanishName))

def usage():
    print("createclinicstation [-h host] [-p port] [-u username] [-w password] [-c clinic] [-s station] [-n name] [-e spanish name] [-l level]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:c:s:n:e:l:")
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
    level = "1"
    spanishName = None
    name = None
    station = None
    clinic = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-c":
            clinic = int(a)
        elif o == "-l":
            level = a
        elif o == "-n":
            name = a
        elif o == "-e":
            spanishName = a
        elif o == "-s":
            station = int(a)
        else:   
            assert False, "unhandled option"
    if clinic == None:
        print("clinic required")
        usage();
    if station == None:
        print("station required")
        usage();
    if name == None:
        print("name required")
        usage();
    if spanishName == None:
        print("spanish name required")
        usage();
    setUp()
    createClinicStation(clinic, station, name, spanishName, level)
if __name__ == "__main__":
    main()
