import json
from collections import OrderedDict
from serviceconnection import ServiceConnection

class ServiceAPI(object):
    def __init__(self):
        self._httpMethod = "POST"
        self._host = None
        self._port = None
        self._url = None
        self._payload = {}

    def setHost(self, host):
        self._host = host

    def getHost(self):
        return self._host

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
