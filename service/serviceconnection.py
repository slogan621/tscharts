#(C) Copyright Syd Logan 2016-2019
#(C) Copyright Thousand Smiles Foundation 2016-2019
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

import requests
import sys
import urllib
from xml.etree import ElementTree
import json
import os

import logging
LOG = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

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
    if request.getToken():
        headers["Authorization"] = "Token {}".format(request.getToken())
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
    proto = "http"
    if request.getPort() == 443:
        proto = "https"
    url = "%s://%s:%d/%s" % (proto, request.getHost(), request.getPort(), request.getURL())

    if isGet:
      try:
        r = requests.get(url, timeout=self._timeout, data=payload, headers=headers, auth=auth, verify=False)
      except requests.exceptions.Timeout:
        timeout = True
    elif isPost:
      try:
        r = requests.post(url, timeout=self._timeout, data=payload, headers=headers, auth=auth, verify=False)
      except requests.exceptions.Timeout:
        timeout = True
    elif isPut:
      try:
        r = requests.put(url, timeout=self._timeout, data=payload, headers=headers, auth=auth, verify=False)
      except requests.exceptions.Timeout:
        timeout = True
    elif isDelete:
      try:
        r = requests.delete(url, timeout=self._timeout, data=payload, headers=headers, auth=auth, verify=False)
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
    return (r.status_code, json_data)

