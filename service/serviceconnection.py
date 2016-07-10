import requests
import sys
import urllib
from xml.etree import ElementTree
import json
import os

import logging
LOG = logging.getLogger(__name__)

class RequestObj():
  pass

class RequestFailed(Exception):

  def __init__(self, url, http_code):
    self._url = url
    self._http_code = int(http_code)

  def __str__(self):
    return repr((self._url, self._http_code))

class ServiceConnection():

  def __init__(self, timeout):
    self._timeout = timeout
    self._auth = None

  def _is_ok(self, r):
    return r.status_code == 200

  def _raise_fail_if(self, url, r, timeout):
    if not self._is_ok(r):
      if timeout:
        j = {"response_code": r.status_code,
             "error_code": 0,
             "msg": "Connection timeout"}
      else:
        try:
          j = r.json()["status"]
        except:
          try:
            t = ElementTree.fromstring(r)
            j = {"response_code": r.status_code,
                 "error_code": 0,
                 "msg": "XML failure response from web server"}

          except:
            j = {"response_code": r.status_code,
                 "error_code": 0,
                 "msg": "Unparsable response from web server"}

      raise RequestFailed(url, j["response_code"], j["error_code"], j["msg"])

  def getAuth(self):
    return self._auth

  def __makeRequest(self, request):

    headers = {"Content-Type": "application/json"}
    timeout = False

    isGet = False
    isPut = False
    isPost = False
    isDelete = False
    if request.getHttpMethod() == "GET":
      isGet = True
    elif request.getHttpMethod() == "POST":
      isPost = True
    elif request.getHttpMethod() == "PUT":
      isPut = True
    elif request.getHttpMethod() == "DELETE":
      isDelete = True

    auth = self.getAuth()

    payload = request.getPayloadAsJSON().encode("utf-8")
    url = "http://%s:%d/%s" % (request.getHost(), request.getPort(), request.getURL())

    if isGet:
      try:
        r = requests.get(url, timeout=self._timeout, data=payload, headers=headers, auth=auth)
      except requests.exceptions.Timeout:
        timeout = True
    elif isPost:
      try:
        r = requests.post(url, timeout=self._timeout, data=payload, headers=headers, auth=auth)
      except requests.exceptions.Timeout:
        timeout = True
    elif isPut:
      try:
        r = requests.put(url, timeout=self._timeout, data=payload, headers=headers, auth=auth)
      except requests.exceptions.Timeout:
        timeout = True
    elif isDelete:
      try:
        r = requests.delete(url, timeout=self._timeout, data=payload, headers=headers, auth=auth)
      except requests.exceptions.Timeout:
        timeout = True

    if timeout:
        r = RequestObj() 
        r.status_code = 500

    json_data = json.loads("{}")
    if r.status_code == 200:
        try:
            json_data = json.loads(r.text.strip())
        except:
            pass

    return (r, json_data)
       
  def makeRequest(self, request):
    r, json_data = self.__makeRequest(request)

    '''
    if r.status_code == 401:
        conf = self.getAuthConf()
        try:
            auth_method = r.headers["WWW-Authenticate"]
        except:
            # RFC 2616 requires a WWW-Authenticate header in 401 responses. If
            # we get here, it was missing. Check if there is configuration that
            # declares an auth method and use that.
            LOG.info("makeRequest: 401 but no WWW-Authenticate")
            auth_method = conf["auth"]
        if auth_method:
            auth_method = auth_method.lower()
            if auth_method == "basic":
                self._auth = requests.HTTPBasicAuth(conf["username"], conf["password"])
            elif auth_method == "digest":
                self._auth = requests.HTTPDigestAuth(conf["username"], conf["password"])
            elif auth_method == "sidauth":
                self._auth = SIDAuth(self.host, self.port, conf["username"], conf["password"])
            else:
                LOG.info("unknown auth {}".format(auth_method))
                # return the 401 here
                return (r.status_code, json_data)
        
            # try again

            r, json_data = self.__makeRequest(request)
    '''

    return (r.status_code, json_data)

