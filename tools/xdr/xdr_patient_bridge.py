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

import os
import tempfile
from datetime import datetime
import getopt
import sys
import time
import subprocess

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

from tschartslib.clinic.clinic import GetClinic
from tschartslib.register.register import GetAllRegistrations
from tschartslib.patient.patient import GetPatient

class XDRPatientRegistrationBridge:

    def __init__(self, host, port, token, xdrbinpath):
        self.host = host
        self.port = port
        self.token = token
        self.clinic = None
        self.processed = []

        if xdrbinpath is None:
            self.xdrbinpath = "c:\XDRClient\bin\XDR.exe"
        else:
            self.xdrbinpath = xdrbinpath 

        x = GetClinic(host, port, token)
        dateStr = datetime.utcnow().strftime("%m/%d/%Y")
        x.setDate(dateStr)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            print("clinic {} on {} exists".format(ret[1]["id"], dateStr))
            self.clinic = ret[1]["id"] 
        elif ret[0] == 404:
            print("no clinic found on {}".format(dateStr))
            sys.exit(2)
        else:
            print("Unable to get clinic, error code {}".format(ret[0]))
            sys.exit(2)

    def pushToXDR(self, patientData):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write("{}-{}, - *{} ({})".format(patientData["paternal_last"], patientData["maternal_last"], patientData["dob"], patientData["id"]))
                tmp.write("PN={}\n".format(patientData["id"]))
                tmp.write("LN={}-{}\n".format(patientData["paternal_last"],
                                        patientData["maternal_last"]))
                tmp.write("FN={}\n".format(patientData["first"]))
                tmp.write("BD={}\n".format(patientData["dob"]))
                tmp.write("SX={}\n".format(patientData["gender"]))
            try:
                ret = subprocess.check_output(['{}'.format(self.xdrbinpath), '{}'.format(path)])
                print("XDR client output for patient {} is {}".format(patientData["id"], ret))
                self.processed.append(patientData["id"])
            except subprocess.CalledProcessError as e:
                print("subprocess CalledProcessError exception in pushToXDR: {}".format(e.output))
            except:
                e = sys.exc_info()[0]
                print("subprocess exception in pushToXDR: {}".format(e))
        finally:
            os.remove(path)

    def processNewRegistrations(self):
        print("looking for new registrations")
        x = GetAllRegistrations(self.host, self.port, self.token)
        x.setClinic(self.clinic)
        ret = x.send(timeout=30)
        if ret[0] == 200:

            # now we have a list of registrations. Each includes
            # an id for the patient registered. Walk this list
            # and create an array of dicts with the patient details
            # that we care about

            registrations = ret[1]
            new_patient_ids = []
            new_patient_data = []

            # get list of new patients

            for x in registrations:
                patient_id = x["patient"]
                if not patient_id in self.processed and not patient_id in new_patient_ids:
                    new_patient_ids.append(x["patient"])

            for x in new_patient_ids:
                y = GetPatient(host, port, token)
                y.setId(x)
                ret = y.send(timeout=30)
                if ret[0] == 200:

                        # got the patient, extract details and add to list

                        patient = ret[1] 

                        p = {}
                        p["id"] = patient["id"]
                        p["first"] = patient["first"]
                        p["middle"] = patient["middle"]
                        p["paternal_last"] = patient["paternal_last"]
                        p["maternal_last"] = patient["maternal_last"]
                        p["dob"] = patient["dob"]
                        p["gender"] = patient["gender"]
                        if patient["id"] not in self.processed:
                            new_patient_data.append(p)
                else:
                    print("Unable to get patient data for patient {} error code {}".format(x, ret[0]))

            # now, create a command and issue to XDR to push the data into
            # their database. pushToXDR will add to processed list if
            # everything is successful

            for x in new_patient_data:
                self.pushToXDR(x)  

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]
    else:
        print("Unable to get access token {}".format(ret[0]))

def usage(app):
    print("{} [-h host] [-p port] [-u username] [-w password] [-x xdr_bin_path]".format(app))
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
    xdrbinpath = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-x":
            xdrbinpath = a
        elif o == "-w":
            password = a
        else:
            usage(sys.argv[0])

    setUp()
    bridge = XDRPatientRegistrationBridge(host, port, token, xdrbinpath)
    while True:
        bridge.processNewRegistrations();
        time.sleep(60)

if __name__ == "__main__":
    main()


