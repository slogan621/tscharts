import getopt, sys
import json
import time

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.register.register import GetAllRegistrations
from test.patient.patient import GetPatient
from test.clinic.clinic import GetAllClinics

class TSSession():
    def __init__(self):
        self.m_host = "127.0.0.1"
        self.m_port = 443
        self.m_username = ""
        self.m_password = ""
        self.m_token = ""

    def setHost(self, host):
        self.m_host = host

    def getHost(self):
        return self.m_host

    def setPort(self, port):
        self.m_port = port

    def getPort(self):
        return self.m_port

    def setUsername(self, username):
        self.m_username = username

    def getUsername(self):
        return self.m_username

    def setPassword(self, password):
        self.m_password = password

    def getPassword(self):
        return self.m_password

    def setToken(self, token):
        self.m_token = token

    def getToken(self):
        return self.m_token

    def login(self):
        retval = True
        login = Login(self.getHost(), self.getPort(), self.getUsername(),
self.getPassword())
        ret = login.send(timeout=30)
        if ret[0] != 200:
            print("failed to login: {}".format(ret[1]))
            retval = False
        else:
            self.setToken(ret[1]["token"])
        return retval

class Clinics():
    def getAllClinics(self, sess):
        x = GetAllClinics(sess.getHost(), sess.getPort(), sess.getToken())
        ret = x.send(timeout=30)
        if ret[0] == 200:
            ret = ret[1]
        else:
            ret = None
        return ret

class Registrations():
    def getPatient(self, sess, id):
        x = GetPatient(sess.getHost(), sess.getPort(), sess.getToken())
        x.setId(id)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            ret = ret[1]
        else:
            ret = None
        return ret

    def getAllRegistrations(self, sess, clinicid):
        patients = []
        x = GetAllRegistrations(sess.getHost(), sess.getPort(), sess.getToken())
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            registrations = ret[1]
            for x in registrations:
                y = self.getPatient(sess, x["patient"])
                if y:
                    p = {}
                    p["first"] = y["first"]
                    p["middle"] = y["middle"]
                    p["paternal_last"] = y["paternal_last"]
                    p["maternal_last"] = y["maternal_last"]
                    p["dob"] = y["dob"]
                    p["gender"] = y["gender"]
                    patients.append(p)
        return patients

def usage():
    print("xrayuploader [-h host] [-p port] -u username -w password") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    session = TSSession()
    host = "127.0.0.1"
    port = 8000
    username = None
    password = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"
    session.setHost(host)
    session.setPort(port)
    session.setUsername(username)
    session.setPassword(password)
    if session.login() == False:
        exit(1)
    regs = Registrations()
    c = Clinics()
    clinics = c.getAllClinics(session)
    for x in clinics:
        print("{}".format(x))   
    
    clinicid = 1
    patientsThisClinic = regs.getAllRegistrations(session, clinicid)
    for x in patientsThisClinic:
        print("{}".format(x))   

if __name__ == "__main__":
    main()
