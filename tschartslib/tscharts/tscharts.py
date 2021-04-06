#(C) Copyright Syd Logan 2017-2021
#(C) Copyright Thousand Smiles Foundation 2017-2021
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
import random

from tschartslib.service.serviceapi import ServiceAPI

class Login(ServiceAPI):
    def __init__(self, host, port, username, password=None, pin=None):
        super(Login, self).__init__()
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)

        if pin and not password:
            payload = {"username": username, "pin": pin}
        elif password and not pin:
            payload = {"username": username, "password": password}
        elif password and pin:
            payload = {"username": username, "password": password, "pin": pin}
        else:
            payload = {"username": username}
        self.setPayload(payload)
        self.setURL("tscharts/v1/login/")

class Logout(ServiceAPI):
    def __init__(self, host, port):
        super(Logout, self).__init__()
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setURL("tscharts/v1/logout/")

class CreateUser(ServiceAPI):
    def __init__(self, host, port, first=None, last=None, password=None, email=None, pin=None):
        super(CreateUser, self).__init__()
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)

        payload = {}
        if first:
            payload["first"] = first
        if last:
            payload["last"] = last
        if password:
            payload["password"] = password
        if email:
            payload["email"] = email
        if pin:
            payload["pin"] = pin

        self.setPayload(payload)

        self.setURL("tscharts/v1/createuser/")

class UpdatePIN(ServiceAPI):
    def __init__(self, host, port, username=None, pin=None):
        super(UpdatePIN, self).__init__()
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)

        payload = {}
        if username:
            payload["username"] = username
        if pin:
            payload["pin"] = pin

        self.setPayload(payload)

        self.setURL("tscharts/v1/updatepin/")

class UpdatePassword(ServiceAPI):
    def __init__(self, host, port, username=None, password=None):
        super(UpdatePassword, self).__init__()
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)

        payload = {}
        if username:
            payload["username"] = username
        if password:
            payload["password"] = password

        self.setPayload(payload)

        self.setURL("tscharts/v1/updatepassword/")

class TestTSCharts(unittest.TestCase):

    testhash = {}

    def setUp(self):
        pass

    # login tests

    def testUpdatePIN(self):
        r = random.randint(1000, 9999)
        first = "test{}".format(r)
        last = "tset{}".format(r)
        email = "test{}@example.com".format(r)
        pword = "testpassword{}".format(r)
        pin = str(r)
        cu = CreateUser(host, port, first, last, pword, email, pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 200)
        r = random.randint(1000, 9999)
        pin = str(r)
        cu = UpdatePIN(host, port, email, pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 200)
        login = Login(host, port, username=email, pin=pin)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdatePassword(self):
        r = random.randint(1000, 9999)
        first = "test{}".format(r)
        last = "tset{}".format(r)
        email = "test{}@example.com".format(r)
        pword = "testpassword{}".format(r)
        pin = str(r)
        cu = CreateUser(host, port, first, last, pword, email, pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 200)
        r = random.randint(1000, 9999)
        pword = "testpassword{}".format(r)
        cu = UpdatePassword(host, port, email, pword)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 200)
        login = Login(host, port, username=email, password=pword)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateUserValid(self):
        r = random.randint(1000, 9999)
        first = "test{}".format(r)
        last = "tset{}".format(r)
        email = "test{}@example.com".format(r)
        pword = "testpassword{}".format(r)
        pin = str(r)
        cu = CreateUser(host, port, first, last, pword, email, pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 200)

        cu = CreateUser(host, port, first, last, pword, email, pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 409)  # already exists

        # try logging in with username and password

        login = Login(host, port, username=email, password=pword)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # try logging in with username and pin

        login = Login(host, port, username=email, pin=pin)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)

        # try logging in with username, password and pin

        login = Login(host, port, username=email, password=pword, pin=pin)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testCreateUserInvalid(self):
        r = random.randint(1000, 9999)
        first = "test{}".format(r)
        last = "tset{}".format(r)
        email = "test{}@example.com".format(r)
        pword = "testpassword{}".format(r)
        pin = str(r)
        cu = CreateUser(host, port, first=first)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

        cu = CreateUser(host, port, last=last)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

        cu = CreateUser(host, port, pin=pin)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

        cu = CreateUser(host, port, first=first, password=pword)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

        cu = CreateUser(host, port, last=last, password=pword)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

        cu = CreateUser(host, port, pin=pin, password=pword)
        ret = cu.send(timeout=30)
        self.assertEqual(ret[0], 400)

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
        self.assertEqual(ret[0], 400)

    def testMissingUsernameMissingPassword(self):
        login = Login(host, port, None, None)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 400)

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
