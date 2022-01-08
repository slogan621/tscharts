#(C) Copyright Syd Logan 2018-2022
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

import getopt, sys
import json
from datetime import datetime

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class GetClinic(ServiceAPI):
    def makeURL(self):
        url = None
        if self._id:
            if self._date != None:
                url = "tscharts/v1/clinic/{}/?date={}".format(self._id,self._date)
            else:
                url = "tscharts/v1/clinic/{}/".format(self._id)
        else:
            if self._date != None:
                url = "tscharts/v1/clinic/?date={}".format(self._date)
            else:
                url = "tscharts/v1/clinic/"
        self.setURL(url)

    def __init__(self, host, port, token, id=None):
        super(GetClinic, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload) 
        self._id = id
        self._date = None
        self.makeURL()

    def setDate(self, date):
        self._date = date
        self.makeURL()

    def getClinicByDate(self, dateStr):
        x = GetClinic(host, port, token)
        x.setDate(dateStr)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("clinic {} on {} exists".format(ret[1]["id"], dateStr))
        elif ret[0] == 404:
            print("no clinic found on {}".format(dateStr))
        else:
            print("Unable to get clinic error code {}".format(ret[0]))

    def getClinic(self):
        x = GetClinic(host, port, token)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("{}".format(ret[1]))
        elif ret[0] == 404:
            print("no clinic found")
        else:
            print("Unable to get clinic error code {}".format(ret[0]))
    
def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]
    else:
        print("Unable to get access token {}".format(ret[0]))

def usage():
    print("getclinic [-h host] [-p port] [-u username] [-w password] [-d datestr]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:d:n")
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
    dateStr = None
    noDateStr = False
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
            dateStr = a
        elif o == "-n":
            noDateStr = True
        else:   
            assert False, "unhandled option"
    if dateStr == None:
        if noDateStr == False:
            dateStr = datetime.utcnow().strftime("%m/%d/%Y") 
   
    setUp()
    gc = GetClinic(host, port, token)
    if dateStr:
        gc.getClinicByDate(dateStr) 
    else:
        gc.getClinic()

if __name__ == "__main__":
    main()
