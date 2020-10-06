#(C) Copyright Xinyue Han 2017-2020
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

import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.medications.medications import CreateMedications, GetMedications

class UpdateMedicationsList():
    def __init__(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        global token
        token = ret[1]["token"]

    def readDrugFromFile(self, filename):
        ret = set()
        try:
            file = open(filename, "r")
        except:
            print("ERROR: File doesn't exist")
            sys.exit()

        for x in file:
            drug = (x.split('\t'))[5].upper().rstrip()
            ret.add(drug)
        file.close()
        return ret      
        
    def createMedications(self):
        druginfile = self.readDrugFromFile(filename)
        newdrug = []
        for medication in druginfile:
            data = {}
            data["name"] = medication
            x = CreateMedications(host, port, token, data)
            ret = x.send(timeout = 30)
            if ret[0] == 200:
                newdrug.append(medication)
        return newdrug
       
    def getMedications(self):
        x = GetMedications(host, port, token)
        ret = x.send(timeout = 30)
        ret = ret[1]
        return ret

def usage():
    print("medications [-h host] [-p port] [-u username] [-w password] [-f filename]") 

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
    global filename
    filename = None
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
            filename = a
        else:   
            assert False, "unhandled option"
   
    x = UpdateMedicationsList()
    druginfile = x.readDrugFromFile(filename)
    print("Current FDA file({}) contains {} drugs.".format(filename, len(druginfile)))
    print("Updating drug list...\n")
    newdrug =  x.createMedications()
    druglist = x.getMedications()

    if len(newdrug) == 0:
        print("No added new drugs\n")
    else:
        print("There are {} added new drugs:".format(len(newdrug)))
        for x in newdrug:
            print(x)
 
    print("Current drug list contains {} drugs.".format(len(druglist)))

if __name__ == "__main__":
    main()
