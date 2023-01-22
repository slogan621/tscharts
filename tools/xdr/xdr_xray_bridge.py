#(C) Copyright Syd Logan 2023
#(C) Copyright Thousand Smiles Foundation 2023
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

from datetime import datetime
import getopt
import sys
import time
import base64
import os
from os import listdir
from os.path import isfile, join

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout
from tschartslib.xray.xray import CreateXRay, GetXRay
from tschartslib.image.image import CreateImage
from tschartslib.clinic.clinic import GetClinic
from tschartslib.register.register import GetAllRegistrations
from tschartslib.patient.patient import GetPatient

class XDRXRayBridge:
    def __init__(self, host, port, token, xdrexportpath):
        self._host = host
        self._port = port
        self._token = token
        self._clinic = None

        if xdrexportpath is None:
            self.xdrexportpath = "c:\XDRClient\exports"
        else:
            self.xdrexportpath = xdrexportpath 

        x = GetClinic(host, port, token)
        dateStr = datetime.utcnow().strftime("%m/%d/%Y")
        x.setDate(dateStr)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("clinic {} on {} exists".format(ret[1]["id"], dateStr))
            self._clinic = ret[1]["id"] 
        elif ret[0] == 404:
            print("no clinic found on {}".format(dateStr))
            sys.exit(2)
        else:
            print("Unable to get clinic, error code {}".format(ret[0]))
            sys.exit(2)

    def uploadXRayImage(self, clinicId, patientId, path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        x = CreateImage(self._host, self._port, self._token)
        x.setPatient(patientId)
        x.setClinic(clinicId)
        x.setType("Xray")
        x.setData(encoded_string)  
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to create patient xray clinic {} patient {} path {} ret {}".format(clinicId, patientId, path, ret[0]))
            return False
        else:
            print("Successfully uploaded patient xray clinic {} patient {}".format(clinicId, patientId))
            return True

    def createXRayRecord(self, clinicId, patientId):    

        # check if we already have an Xray record for this
        # patient, clinic pair. If we do, return

        x = GetXRay(self._host, self._port, self._token)
        x.setPatient(patientId)
        x.setClinic(clinicId)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            # already exists, no further work needed
            return True

        # create a record. defaults may not reflect 
        # reality but can be changed by user on the 
        # tablet. 

        x = CreateXRay(self._host, self._port, self._token)
        x.setPatient(patientId)
        x.setClinic(clinicId)
        x.setMouthType("child")
        x.setTeeth(0)
        x.setXRayType("anteriors_bitewings")
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to create XRay record clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))
            return False
        else:
            print("Successfully created XRay record clinic {} patient {}".format(clinicId, patientId))
            return True

    def processNewXRayExports(self):
        print("looking for new xray exports from XDR")
        files = [f for f in listdir(self.xdrexportpath) if isfile(join(self.xdrexportpath, f))]
        for x in files:
            patientId = int(x.split('_')[0])
            if "uploaded" in x.split('.'):
                # skip already uploaded files
                continue
            path = join(self.xdrexportpath, x)
            if self.createXRayRecord(self._clinic, patientId) and self.uploadXRayImage(self._clinic, patientId, path):
                os.rename(path, "{}.uploaded".format(path))

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]
    else:
        print("Unable to get access token {}".format(ret[0]))

def usage(app):
    print("{} [-h host] [-p port] [-u username] [-w password] [-x xdr_export_path]".format(app))
    sys.exit(2)

def main(): 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:x:")
    except getopt.GetoptError as err:
        print(str(err))
        usage(sys.argv[0])
    global host
    host = "127.0.0.1"
    global port
    port = 443
    global username
    username = None
    global password
    password = None
    xdrexportpath = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-x":
            xdrexportpath = a
        elif o == "-w":
            password = a
        else:
            usage(sys.argv[0])

    setUp()
    if xdrexportpath and (not os.path.exists(xdrexportpath)):
        os.makedirs(xdrexportpath)

    bridge = XDRXRayBridge(host, port, token, xdrexportpath)
    while True:
        bridge.processNewXRayExports();
        time.sleep(60)

if __name__ == "__main__":
    main()


