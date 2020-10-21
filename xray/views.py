#(C) Copyright Syd Logan 2019-2020
#(C) Copyright Thousand Smiles Foundation 2019-2020
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
from xray.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

import logging
LOG = logging.getLogger("tscharts")

class XRayView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def mouthTypeToName(self, t):
        mouthTypeToNameMap = {'a': "adult", 'c': "child"}

        ret = None
        try:
            ret = mouthTypeToNameMap[t] 
        except:
            pass
        return ret

    def nameToMouthType(self, name):
        nameToMouthTypeMap = {"adult": 'a', "child": 'c'}

        ret = None
        try:
            ret = nameToMouthTypeMap[name] 
        except:
            pass
        return ret

    def xrayTypeToName(self, t):
        xrayTypeToNameMap = {'f': "full",
                         'a': "anteriors_bitewings",
                         'p': "panoramic_view",
                         'c': "cephalometric",
        }

        ret = None
        try:
            ret = xrayTypeToNameMap[t]
        except:
            pass
        return ret

    def nameToXrayType(self, name):
        nameToXrayTypeMap = {"full": 'f',
                         "anteriors_bitewings": 'a',
                         "panoramic_view": 'p',
                         "cephalometric": 'c',
        }

        ret = None
        try:
            ret = nameToXrayTypeMap[name]
        except:
            pass
        return ret

    def convertCSVToDBXrayType(self, val):
        csv = val.replace(" ", "").split(',')
        typestr = ""
        try:
            for x in csv:
                typestr = typestr + self.nameToXrayType(x)
        except:
            typestr = ""

        return typestr

    def convertFromDBXrayTypeToCSV(self, val):

        y = []

        try:
            for x in val:
                y.append(self.xrayTypeToName(x))
        except:
            y = []

        # create CSV

        typestr = ""
        for x in y:
            typestr = typestr + x
            typestr = typestr + " "

        typestr = typestr.rstrip().replace(" ", ",")

        return typestr

    def serialize(self, entry):
        
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["time"] = entry.time.strftime("%m/%d/%Y")
        m["xray_type"] = self.convertFromDBXrayTypeToCSV(entry.type)
        
        m["mouth_type"] = self.mouthTypeToName(entry.mouthtype)
        m["teeth"] = entry.teeth 

        return m

    @log_request
    def get(self, request, xray_id=None, format=None):
        xray = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if xray_id:
            try:
                xray = XRay.objects.get(id = xray_id)
            except:
                xray = None
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

            if not aClinic and not aPatient:
                badRequest = True

            if not badRequest and len(kwargs):
                try:
                    xray = XRay.objects.filter(**kwargs)
                except:
                    xray = None

        if not xray and not badRequest:
            raise NotFound
        elif not badRequest:
            if xray_id:
                ret = self.serialize(xray)
            else:
                ret = []
                for x in xray:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = {} 

        try:
            val = data["mouth_type"] 
            kwargs["mouthtype"] = self.nameToMouthType(val)
            if kwargs["mouthtype"] == None:
                valid = False
            val = data["xray_type"] 
            #kwargs["type"] = self.nameToXrayType(val)
            kwargs["type"] = self.convertCSVToDBXrayType(val)
            if kwargs["type"] == "":
                valid = False
            if not "clinic" in data:
                valid = False
            else:
                kwargs["clinic"] = data["clinic"]
            if not "patient" in data:
                valid = False
            else:
                kwargs["patient"] = data["patient"]
            if not "teeth" in data:
                valid = False
            else:
                kwargs["teeth"] = int(data["teeth"])
        except:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, xray):
        valid = True
        sawType = False
        sawTeeth = False
        sawMouthType = False

        try:
            if "xray_type" in data:
                val = data["xray_type"] 
                xray.type = self.convertCSVToDBXrayType(val)
                if xray.type == "":
                    valid = False
                else:
                    sawType = True
            if valid and "mouth_type" in data:
                val = data["mouth_type"] 
                xray.mouthtype = self.nameToMouthType(val)
                if xray.mouthtype == None:
                    valid = False
                else:
                    sawMouthType = True
            if valid and "teeth" in data:
                xray.teeth = int(data["teeth"])
                sawTeeth = True
        except:
            valid = False

        if valid and (sawType == False and sawMouthType == False and sawTeeth == False):
            valid = False
        return valid, xray

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
                kwargs["patient"] = aPatient
                kwargs["clinic"] = aClinic
                xray = XRay(**kwargs)
                if xray:
                    xray.save()
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
            return Response({'id': xray.id})

    @log_request
    def put(self, request, xray_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not xray_id:
            badRequest = True

        if not badRequest:
            xray = None

            try:
                xray = XRay.objects.get(id=xray_id)
            except:
                pass

            if not xray:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, xray = self.validatePutArgs(data, xray)
                    if valid: 
                        xray.save()
                    else:
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
                    LOG.info(u'xray put: Exception trying to update xray {} {}'.format(sys.exc_info()[0], xray.__dict__))
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})
       
    @log_request 
    def delete(self, request, xray_id=None, format=None):
        xray = None

        # see if the xray object exists

        if not xray_id:
            return HttpResponseBadRequest()
        try:
            xray = XRay.objects.get(id=xray_id)
        except:
            xray = None

        if not xray:
            raise NotFound
        else:
            xray.delete()

        return Response({})
