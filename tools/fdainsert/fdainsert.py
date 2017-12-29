import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

def drug_set(file_name):
    ret = set()
    file_opened = open(file_name,"r")
    for line in file_opened:
        drug = (line.split('\t'))[5].upper().rstrip()
        ret.add(drug)
    file_opened.close()
    return ret

class CreateMedications(ServiceAPI):
    def __init__(self, host, port, token, payload):
        super(CreateMedications, self).__init__()

        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setPayload(payload)
        self.setURL("tscharts/v1/medications/")

class GetMedications(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetMedications, self).__init__()
      
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/medications/")

class DeleteMedications(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteMedications, self).__init__()
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/medications/{}/".format(id))

class AcquireMedicationsList():
    def __init__(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        global token
        token = ret[1]["token"]
        
    def createMedications(self):
        aset = drug_set("Products.txt")
        new_drug = []
        for medication in aset:
            data = {}
            data["name"] = medication
            x = CreateMedications(host, port, token, data)
            ret = x.send(timeout = 30)
            if ret[0] == 200:
                new_drug.append(medication)
        return new_drug
       
    def getMedications(self):
        x = GetMedications(host, port, token)
        ret = x.send(timeout = 30)
        ret = ret[1]
        return ret
    
def usage():
    print("medications [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
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

    x = AcquireMedicationsList()
    new_drug =  x.createMedications()
    drug_list = x.getMedications()

    if len(new_drug) == 0:
        print("No added new drugs")
    else:
        print("There are {} added new drugs:{}.".format(len(new_drug), ",".join(str(x) for x in new_drug)))

    print("Current drug list contains {} drugs.".format(len(drug_list)))

if __name__ == "__main__":
    main()

