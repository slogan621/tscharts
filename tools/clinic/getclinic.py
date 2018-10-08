'''
unit tests for clinic application. Assumes django server is up
and running on the specified host and port
'''

import getopt, sys
import json
from datetime import datetime

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

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
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:d:")
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
        else:   
            assert False, "unhandled option"
    if dateStr == None:
        dateStr = datetime.utcnow().strftime("%m/%d/%Y") 
   
    setUp()
    gc = GetClinic(host, port, token)
    gc.getClinicByDate(dateStr) 

if __name__ == "__main__":
    main()
