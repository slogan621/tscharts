#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
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

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.covidvac.covidvac import CreateCOVIDVac, GetCOVIDVac

class UpdateCOVIDVacList():
    def __init__(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        global token
        token = ret[1]["token"]

    def parseCOVIDVacFile(self, filename):
        ret = []
        try:
            file = open(filename, "r")
        except:
            print("ERROR: File doesn't exist")
            sys.exit()

        line = 0
        for x in file:
            line = line + 1
            x = x.strip()
            if len(x) == 0:
                continue
            if x[0] == "#":  # comment
                continue

            ret.append(x)    
        file.close()
        print("{}".format(ret))
        return ret      
        
    def uploadCOVIDVacs(self, path):
        data = self.parseCOVIDVacFile(path)
        for x in data:
            val = {}
            val["name"] = x
            c = CreateCOVIDVac(host, port, token, val)
            ret = c.send(timeout = 30)
            if ret[0] != 200:
                print("unable to create COVIDVac entry {}".format(val))
       
def usage():
    print("covidinsert [-h host] [-p port] [-u username] [-w password] -f path") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:f:")
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
    path = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-f":
            path = a
        else:   
            assert False, "unhandled option"
   
    x = UpdateCOVIDVacList()
    x.uploadCOVIDVacs(path)

if __name__ == "__main__":
    main()
