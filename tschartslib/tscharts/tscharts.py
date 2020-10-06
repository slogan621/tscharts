#(C) Copyright Syd Logan 2017-2020
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

'''
unit tests for tscharts application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from tschartslib.service.serviceapi import ServiceAPI

class Login(ServiceAPI):
    def __init__(self, host, port, username, password):
        super(Login, self).__init__()
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)

        payload = {"username": username, "password": password}
        self.setPayload(payload)
        self.setURL("tscharts/v1/login/")

class Logout(ServiceAPI):
    def __init__(self, host, port):
        super(Logout, self).__init__()
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setURL("tscharts/v1/logout/")

class TestTSCharts(unittest.TestCase):

    def setUp(self):
        pass

    # login tests

    def testMissingUsernameWithPassword(self):
        login = Login(host, port, None, "abcdefg")
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 403)

    def testUnknownUsernameWithPassword(self):
        login = Login(host, port, "sdfsfsfsd", "abcdefg")
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 403)

    def testUnknownUsernameMissingPassword(self):
        login = Login(host, port, "sdfsfsfsd", None)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 403)

    def testMissingUsernameMissingPassword(self):
        login = Login(host, port, None, None)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 403)

    def testInvalidPassword(self):
        validUser = username
        invalidPassword = "sdfsfsdfscewe"
        login = Login(host, port, validUser, invalidPassword)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 403)

    def testValidLogin(self):
        validUser = username
        validPassword = password
        login = Login(host, port, validUser, validPassword)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])

    # logout tests

    def testLogoutNotLoggedIn(self):
        # logout user first, then logout a second time
       
        self.testValidLogin()  
        logout = Logout(host, port)
        ret = logout.send(timeout=30)
        self.assertEqual(ret[0], 200)
        logout = Logout(host, port)
        ret = logout.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testLogoutLoggedIn(self):
        self.testValidLogin()  
        logout = Logout(host, port)
        ret = logout.send(timeout=30)
        self.assertEqual(ret[0], 200)

def usage():
    print("tscharts [-h host] [-p port] [-u username] [-w password]") 

def main(rgv=[sys.argv[0]]):
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
