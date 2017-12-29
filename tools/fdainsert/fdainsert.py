import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.medications.medications import CreateMedications, GetMedications

class UpdateMedicationsList():
    def __init__(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        global token
        token = ret[1]["token"]

    def readDrugFromFile(self, filename):
        ret = set()
        file = open(filename, "r")
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
    print("Current fda file({}) contains {} drugs.".format(filename, len(druginfile)))
    print("Updating drug list...")
    newdrug =  x.createMedications()
    druglist = x.getMedications()

    if len(newdrug) == 0:
        print("No added new drugs")
    else:
        print("There are {} added new drugs:{}.".format(len(newdrug), ",".join(str(x) for x in newdrug)))

    print("Current drug list contains {} drugs.".format(len(druglist)))

if __name__ == "__main__":
    main()
