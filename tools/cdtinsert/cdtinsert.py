#(C) Copyright Syd Logan 2020
#(C) Copyright Thousand Smiles Foundation 2020
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
from tschartslib.dentalcdt.dentalcdt import CreateDentalCDT, GetDentalCDT

class UpdateCDTList():
    def __init__(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        global token
        token = ret[1]["token"]

    def parseCDTFile(self, filename):
        ret = []
        try:
            file = open(filename, "r")
        except:
            print("ERROR: File doesn't exist")
            sys.exit()

        catdata = {}
        catdata["category"] = None
        catdata["values"] = []
        haveCatData = False
        line = 0
        for x in file:
            line = line + 1
            x = x.strip()
            if len(x) == 0:
                continue
            if x[0] == "#":  # comment
                continue

            if "CATEGORY=" in x.upper():
                if haveCatData == True:
                    ret.append(catdata)
                    catdata = {}
                    catdata["category"] = None
                    catdata["values"] = []
                    haveCatData = False
                category = x.split('=')[1].strip()
                if len(category): 
                    catdata["category"] = category.strip()
                else:
                    print("syntax error: line {}: malformed category {}".format(line, x))
            elif catdata["category"]:
                code = None
                desc = None
                try:
                    l = x.split(" ", 1)
                    code = l[0]
                    desc = l[1]
                except:
                    print("syntax error: line {}: {} malformed".format(line, x))
                    continue
                if not len(code) == 5:
                    print("syntax error: line {}: {} invalid length code. Format is Dnnnn, where n is digit".format(line, x))
                    continue
                if not code[0] == 'D' and code[0] != 'd':
                    print("syntax error: line {}: {} Invalid code, missing 'D'. Format is Dnnnn, where n is digit".format(line, x))
                    continue
                code = code.capitalize()
                if not code[1:].isdigit():
                    print("syntax error: line {}: {} Invalid code, non-numeric. Format is Dnnnn, where n is digit".format(line, x))
                    continue
                val = {}
                val["code"] = code
                val["desc"] = desc
                catdata["values"].append(val) 
                haveCatData = True
        file.close()
        print("{}".format(ret))
        return ret      
        
    def uploadCDTs(self, path):
        data = self.parseCDTFile(path)
        for x in data:
            for y in x["values"]:
                if self.getCDT(y["code"]) == 200:
                    continue
                y["category"] = x["category"]
                c = CreateDentalCDT(host, port, token, y)
                ret = c.send(timeout = 30)
                if ret[0] != 200:
                    print("unable to create CDT code {}".format(y))
       
    def getCDT(self, code):
        x = GetDentalCDT(host, port, token)
        x.setCode(code)
        ret = x.send(timeout = 30)
        return ret[0]

def usage():
    print("cdtinsert [-h host] [-p port] [-u username] [-w password] -f path") 

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
   
    x = UpdateCDTList()
    x.uploadCDTs(path)

if __name__ == "__main__":
    main()
