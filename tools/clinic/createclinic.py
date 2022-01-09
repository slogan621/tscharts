#(C) Copyright Syd Logan 2018-2022
#(C) Copyright Thousand Smiles Foundation 2018-2022
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
from datetime import datetime, timedelta
import json
import dateinmonth

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.clinic.clinic import CreateClinic

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]

def createClinic(location, clinicDate, duration):
    datet = clinicDate.split('/')
    start = datetime(int(datet[2]), int(datet[0]), int(datet[1]))
    end = start + timedelta(days=duration)
    sstr = start.strftime("%m/%d/%Y") 
    estr = end.strftime("%m/%d/%Y") 
    print("start {} {} end {} {}".format(start, sstr, end, estr))
    x = CreateClinic(host, port, token, location, sstr, estr)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        print("created clinic with id {}".format(ret[1]["id"]))
    else:
        print("failed to create clinic")

def usage():
    print("createclinic [-h host] [-p port] [-u username] [-w password] [-d duration] [-l location] [-c clinicdate (MM/DD/YYYY)] [-x]") 
    print("specify either -c or -x. -x will create a clinic on the first Friday of each of the following months in the current calendar year: Feb, May, Aug, Nov");
    sys.exit(0)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:c:s:d:l:c:x")
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
    duration = None
    location = None
    clinicDate = None
    createNext = False
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-d":
            duration = int(a)
        elif o == "-l":
            location = a
        elif o == "-c":
            clinicDate = a
        elif o == "-x":
            createNext = True
        else:   
            assert False, "unhandled option"
    if duration == None:
        print("duration required")
        usage();
    if location == None:
        print("location required")
        usage();
    if clinicDate == None and createNext == False:
        print("clinic date or -x required")
        usage();
    setUp()
    if createNext == True:
        year = datetime.now().year
        for month in [2, 5, 8, 11]:
            adate = dateinmonth.GetNthDateInMonth(year, month, 1, 6)
            adate = adate.strftime("%m/%d/%Y")
            createClinic(location, adate, int(duration))
    else:
        createClinic(location, clinicDate, int(duration))
if __name__ == "__main__":
    main()
