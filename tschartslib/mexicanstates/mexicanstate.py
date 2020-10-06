# -*- coding: UTF-8 -*-

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

'''
unit tests for mexicanstates application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI
from tschartslib.tscharts.tscharts import Login, Logout

class GetAllMexicanStates(ServiceAPI):
    def __init__(self, host, port, token):
        super(GetAllMexicanStates, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/mexicanstates/")

class TestTSMexicanStates(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testGetAllMexicanStates(self):

        statenames = [u"Aguascalientes",
                      u"Baja California",
                      u"Baja California Sur",
                      u"Chihuahua",
                      u"Colima",
                      u"Campeche",
                      u"Coahuila",
                      u"Chiapas",
                      u"Federal District",
                      u"Durango",
                      u"Guerrero",
                      u"Guanajuato",
                      u"Hidalgo",
                      u"Jalisco",
                      u"México State",
                      u"Michoacán",
                      u"Morelos",
                      u"Nayarit",
                      u"Nuevo León",
                      u"Oaxaca",
                      u"Puebla",
                      u"Querétaro",
                      u"Quintana Roo",
                      u"Sinaloa",
                      u"San Luis Potosí",
                      u"Sonora",
                      u"Tabasco",
                      u"Tlaxcala",
                      u"Tamaulipas",
                      u"Veracruz",
                      u"Yucatán",
                      u"Zacatecas",
                     ]

        x = GetAllMexicanStates(host, port, token)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        states = ret[1]
        self.assertTrue(len(states) == len(statenames))
        for x in states:
            self.assertTrue(x in statenames)

def usage():
    print("mexicanstates [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
    except getopt.GetoptError as err:
        print(str(err))
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
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
