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

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from register.models import *
from clinic.models import *
from patient.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class RegisterView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["timein"] = entry.timein
        m["timeout"] = entry.timeout
        if entry.state == 'i':
            m["state"] = "Checked In"
        else:
            m["state"] = "Checked Out"
        return m

    @log_request
    def get(self, request, register_id=None, format=None):
        register = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if register_id:
            try:
                register = Register.objects.get(id = register_id)
            except:
                register = None
        else:
            # look for optional arguments
            patientid = request.GET.get("patient", '')
            if patientid and patientid != '':
                try:
                    aPatient = Patient.objects.get(id=patientid)
                    if not aPatient:
                        badRequest = True
                    else:
                        kwargs["patient"] = aPatient
                except:
                    badRequest = True

            clinicid = request.GET.get("clinic", '')
            if clinicid and clinicid != '':
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                    if not aClinic:
                        badRequest = True
                    else:
                        kwargs["clinic"] = aClinic
                except:
                    badRequest = True

            try:
                state = data["state"]
                if state != "Checked In" and state != "Checked Out":
                    badRequest = True
                else:
                    if state == "Checked In": 
                        kwargs["state"] = 'i';
                    else:
                        kwargs["state"] = 'o';
            except:
                pass # no state

            if not badRequest:
                try:
                    register = Register.objects.filter(**kwargs)
                except:
                    register = None

        if not register and not badRequest:
            raise NotFound
        elif not badRequest:
            if register_id:
                ret = self.serialize(register)
            else:
                ret = []
                for x in register:
                    ret.append(self.serialize(x))
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if "state" in data:
            if not (data["state"] == "Checked In" or data["state"] == "Checked Out"):
                valid = False
            else:
                if data["state"] == "Checked In":
                    kwargs["state"] = "i"
                else:
                    kwargs["state"] = "o"

        return valid, kwargs

    def validatePutArgs(self, data, register):
        valid = True

        try:
            if "state" in data:
                if not (data["state"] == "Checked In" or data["state"] == "Checked Out"):
                    valid = False
                else:
                    if data["state"] == "Checked In":
                        register.state = 'i'
                        register.timein = datetime.now()
                    else:
                        register.state = 'o'
                        register.timeout = datetime.now()
            else:
                valid = False
        except:
            valid = False

        return valid, register

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True

        # validate the post data, and get a kwargs dict for
        # creating the object 

        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            badRequest = True

        if not badRequest:

            # get the instances

            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None
 
            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None

            if not aPatient or not aClinic:
                raise NotFound

        if not badRequest:
            try:
                kwargs["clinic"] = aClinic
                kwargs["patient"] = aPatient
                register = Register(**kwargs)
                if register:
                    register.save()
                else:
                    implError = True
            except Exception as e:
                implError = True
                implMsg = sys.exc_info()[0] 

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': register.id})

    @log_request
    def put(self, request, register_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not register_id:
            badRequest = True

        if not badRequest:
            register = None

            try:
                register = Register.objects.get(id=register_id)
            except:
                pass

            if not register:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, register = self.validatePutArgs(data, register)
                    if valid: 
                        register.save()
                    else:
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})
       
    @log_request 
    def delete(self, request, register_id=None, format=None):
        register = None

        # see if the state change object exists

        if not register_id:
            return HttpResponseBadRequest()
        try:
            register = Register.objects.get(id=register_id)
        except:
            register = None

        if not register:
            raise NotFound
        else:
            register.delete()

        return Response({})
