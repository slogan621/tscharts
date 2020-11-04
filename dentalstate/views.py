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

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from clinic.models import *
from patient.models import *
from dentalstate.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import traceback

import sys
import json

import logging

LOG = logging.getLogger("tscharts")

class DentalStateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    integerFields = [
        "tooth",
    ]

    booleanFields = [
    ]

    textFields = [
        "username",
  	"comment",
    ]

    stateFields = [
        "state",
    ]

    def stateToString(self, val):
        ret = None
        for x in DentalState.DENTAL_STATE_CHOICES:
            if x[0] == val:
                ret = x[1]
                break
        return ret

    def stringToState(self, val):
        ret = None
        for x in DentalState.DENTAL_STATE_CHOICES:
            if x[1] == val:
                ret = x[0]
                break
        return ret

    def stringToBoolean(self, val):
        ret = None 
        if val == "true" or val == "True":
            ret = True
        elif val == "false" or val == "False":
            ret = False
        return ret    

    def booleanToString(self, val):
        ret = None 
        if val == True:
            ret = "true"
        elif val == False:
            ret = "false"
        return ret    

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["username"] = entry.username
        m["time"] = entry.time

        m["tooth"] = entry.tooth
        m["code"] = entry.code_id

        m["state"] = self.stateToString(entry.state)

        m["comment"] = entry.comment

        return m

    @log_request
    def get(self, request, dental_state_id=None, format=None):
        dental_state = None
        badRequest = False
        aPatient = None
        aClinic = None
        aCode = None
        kwargs = {}

        if dental_state_id:
            try:
                dental_state = DentalState.objects.get(id = dental_state_id)
            except:
                dental_state = None
        else:
            # look for optional arguments
            try:
                patientid = request.GET.get('patient', '')
                if patientid != '':
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        if not aPatient:
                            badRequest = True
                        else:
                            kwargs["patient"] = aPatient
                    except:
                        badRequest = True
            except:
                pass # no patient ID

            try:
                clinicid = request.GET.get('clinic', '')
                if clinicid != '':
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        if not aClinic:
                            badRequest = True
                        else:
                            kwargs["clinic"] = aClinic
                    except:
                        badRequest = True
            except:
                pass # no clinic ID

            try:
                codeid = request.GET.get('code', '')
                if codeid != '':
                    try:
                        aCode = DentalCDT.objects.get(id=codeid)
                        if not aCode:
                            badRequest = True
                        else:
                            kwargs["code"] = aCode
                    except:
                        badRequest = True
            except:
                pass # no code ID

            for x in self.stateFields:
                try:
                    val = request.GET.get(x, '')
                    if val != '':
                        val = self.stringToState(val)
                        if val == None:
                            badRequest = True
                        else:
                            kwargs[x] = val
                except:
                    pass

            for x in self.integerFields:
                try:
                    val = request.GET.get(x, '')
                    if val != '':
                        val = int(val)
                        if val == None:
                            badRequest = True
                        else:
                            kwargs[x] = val
                except:
                    pass

            for x in self.textFields:
                try:
                    val = request.GET.get(x, '')
                    if val != '':
                        if x == "comment":
                            kwargs["comment__icontains"] = val
                        elif x == "username":
                            kwargs["username__icontains"] = val
                except:
                    pass

            if not badRequest:
                try:
                    dental_state = DentalState.objects.filter(**kwargs)
                except:
                    dental_state = None

        if not dental_state and not badRequest:
            raise NotFound
        elif not badRequest:
            if dental_state_id:
                ret = self.serialize(dental_state)
            else:
                ret = []
                for x in dental_state:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = {}
        kwargs = data

        for k, v in data.items():
            if not k in self.stateFields and not k in self.booleanFields and not k in self.textFields and not k in self.integerFields and k != "patient" and k != "clinic" and k != "code":
                valid = False
                LOG.warning("validatePostArgs: Failed to validate key {} value {}".format(k, v))
                break

        try:
            val = self.stringToState(data["state"])
            if val == None:
                LOG.warning("validatePostArgs: Failed to validate key state val {}".format(data["state"]))
                valid = False
            else:
                kwargs["state"] = val
        except:
            LOG.warning("validatePostArgs: Failed to locate key {}: {}".format("state", sys.exc_info()[0]))
            valid = False

        try:
            if not ("username" in data and len(data["username"]) > 0):
                valid = False
                LOG.warning("validatePostArgs: Failed to validate key username")
            else:
                kwargs["username"] = data["username"]
        except:
            LOG.warning("validatePostArgs: Exception: Failed to validate key username")
            valid = False

        for x in self.booleanFields:
            try: 
                val = self.stringToBoolean(data[x])
                if val == None:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                LOG.warning("validatePostArgs: Failed to locate key x {}".format(x))
                valid = False

        for x in self.integerFields:
            try: 
                LOG.warning("validatePostArgs: validating key x {} val {}".format(x, data[x]))
                val = int(data[x])
                if val == None:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                LOG.warning("validatePostArgs: Failed to locate key x {} {}".format(x, sys.exc_info()[0]))
                valid = False

        for x in self.textFields:
            try: 
                val = str(data[x])
                if val == False:
                    LOG.warning("validatePostArgs: Failed to validate key x {} val {}".format(x, data[x]))
                    valid = False
                    break
                else:
                    kwargs[x] = data[x]
            except:
                LOG.warning("validatePostArgs: Failed to locate key x {}".format(x))
                valid = False

        return valid, kwargs

    def validatePutArgs(self, data, dental_state):
        valid = True
        found = False

        # first check to see if we have at least one item, and what
        # we have is paired with a valid value

        for k, v in data.items():

            if k in self.stateFields:
                found = True
                try:
                    z = self.stringToState(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.booleanFields:
                found = True
                try:
                    z = self.stringToBoolean(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.integerFields:
                found = True
                try:
                    z = int(v)
                    if z == None:
                        LOG.warning("validatePutArgs: invalid k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid k {} v {}".format(k, v))
                    valid = False

            elif k in self.textFields:
                found = True
                try:
                    x = str(v)
                    if x == None:
                        LOG.warning("validatePutArgs: invalid text field k {} v {}".format(k, v))
                        valid = False
                except:
                    LOG.warning("validatePutArgs: exception invalid text field k {} v {}".format(k, v))
                    valid = False
            elif k in ["clinic", "patient", "id", "code"]:
                found = True
            else:
                LOG.warning("validatePutArgs: unknown key k {} v {}".format(k, v))
                valid = False # unknown key

        # now, build up the dental state object

        if found == True and valid == True:
            for k, v in data.items():
                LOG.warning("validatePutArgs: bottom loop k {} v {}".format(k, v))
                if k == "tooth":
                    dental_state.tooth = int(v)
                elif k == "state":
                    dental_state.state = self.stringToState(v)
                elif k == "username":
                    dental_state.username = str(v)
  	        elif k == "comment":
                    dental_state.comment = str(v)

            try:
                if "clinic" in data:
                    aClinic = Clinic.objects.get(id=int(data["clinic"]))
                    dental_state.clinic = aClinic 
            except:
                LOG.warning("validatePutArgs: invalid clinic {}".format(data["clinic"]))
                valid = False

            try:
                if "patient" in data:
                    aPatient = Patient.objects.get(id=int(data["patient"]))
                    dental_state.patient = aPatient
            except:
                LOG.warning("validatePutArgs: invalid patient {}".format(data["patient"]))
                valid = False

            try:
                if "code" in data:
                    aCode = DentalCDT.objects.get(id=int(data["code"]))
                    dental_state.code = aCode
            except:
                LOG.warning("validatePutArgs: invalid patient {}".format(data["patient"]))
                valid = False

        return valid, dental_state

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False
        implMsg = ""

        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True

        try:
            codeid = int(data["code"])
        except:
            badRequest = True

        # validate the post data, and get a kwargs dict for
        # creating the object 

        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            LOG.warning("post: Failed to validate!!")
            badRequest = True

        if not badRequest and not implError:

            # get the instances

            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None
 
            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None

            try:
                aCode = DentalCDT.objects.get(id=codeid)
            except:
                aCode = None

            if not aPatient or not aClinic or not aCode:
                raise NotFound

        if not badRequest and not implError:
            try:
                kwargs["patient"] = aPatient
                kwargs["clinic"] = aClinic
                kwargs["code"] = aCode
                dental_state = DentalState(**kwargs)
                if dental_state:
                    dental_state.save()
                else:
                    LOG.warning("post: unable to create DentalState object!!")
                    badRequest = True
            except Exception as e:
                badRequest = True
                LOG.warning("post: exception!! {}".format(traceback.format_exc()))
                implMsg = sys.exc_info()[0] 

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': dental_state.id})

    @log_request
    def put(self, request, dental_state_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not dental_state_id:
            LOG.warning("put: missing ID arg")
            badRequest = True

        if not badRequest:
            dental_state = None

            try:
                dental_state = DentalState.objects.get(id=dental_state_id)
            except:
                LOG.warning("DentalState put exception!!")

            if not dental_state:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, dental_state = self.validatePutArgs(data, dental_state)
                    if valid: 
                        dental_state.save()
                    else:
                        LOG.warning("put: validate put args failed")
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
                    LOG.warning("DentalState exception {}".format(implMsg))
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})

    @log_request 
    def delete(self, request, dental_state_id=None, format=None):
        dental_state = None

        # see if the object exists

        if not dental_state_id:
            return HttpResponseBadRequest()
        try:
            dental_state = DentalState.objects.get(id=dental_state_id)
        except:
            dental_state = None

        if not dental_state:
            raise NotFound
        else:
            dental_state.delete()

        return Response({})
