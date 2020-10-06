#(C) Copyright Syd Logan 2018-2020
#(C) Copyright Thousand Smiles Foundation 2018-2020
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

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    global token
    token = ret[1]["token"]

class GetStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(GetStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/station/{}/".format(id))

class GetAllStations(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllStations, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/station/")

def getStation(id):
    x = GetStation(host, port, token, id)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        ret = ret[1]
        print("station id {} is '{}'".format(id, ret["name"]))
    else:
        print("unable to get station with id {}: ret {}".format(id, ret[0]))
    
def getAllStations():
    x = GetAllStations(host, port, token)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        stations = ret[1]
        for x in stations:
            print("id {} name {} level {}".format(x["id"], x["name"], x["level"]))
    else:
        print("unable to get stations: ret {}".format(ret[0]))

def usage():
    print("station [-h host] [-p port] [-u username] [-w password] [-i id]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:i:")
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
        else:   
            assert False, "unhandled option"
    setUp()
    if id == None:
        getAllStations()
    else:
        getStation(id)

if __name__ == "__main__":
    main()
