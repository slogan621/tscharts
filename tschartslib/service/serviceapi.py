#(C) Copyright Syd Logan 2016-2020
#(C) Copyright Thousand Smiles Foundation 2016-2020
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

import json
from collections import OrderedDict
from tschartslib.service.serviceconnection import ServiceConnection

class ServiceAPI(object):
    def __init__(self):
        self._httpMethod = "POST"
        self._host = None
        self._port = None
        self._token = None
        self._url = None
        self._payload = {}

    def setHost(self, host):
        self._host = host

    def getHost(self):
        return self._host

    def setToken(self, token):
        self._token = token

    def getToken(self):
        return self._token

    def setPort(self, port):
        self._port = port

    def getPort(self):
        return self._port

    def setURL(self, url):
        self._url = url

    def getURL(self):
        return self._url

    def setHttpMethod(self, method):
        self._httpMethod = method

    def getHttpMethod(self):
        return self._httpMethod
        
    def setPayload(self, payload):
        self._payload = payload

    def getPayload(self):
        return self._payload

    def getPayloadAsJSON(self):
        return json.dumps(OrderedDict(self.getPayload()))

    def send(self, timeout):
        conn = ServiceConnection(timeout) 
        r = conn.makeRequest(self)
        return r
