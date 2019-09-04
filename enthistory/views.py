#(C) Copyright Syd Logan 2019
#(C) Copyright Thousand Smiles Foundation 2019
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
from enthistory.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTHistoryView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def ENTTypeToString(self, val):
        ret = None 
        data = {ENTHistory.ENT_TYPE_HEARING_LOSS:"hearing loss",
                ENTHistory.ENT_TYPE_DRAINAGE:"drainage", 
                ENTHistory.ENT_TYPE_PAIN:"pain",
                ENTHistory.ENT_TYPE_OTHER:"other"}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToENTType(self, val):
        ret = None
        data = {"hearing loss":ENTHistory.ENT_TYPE_HEARING_LOSS,
                "drainage":ENTHistory.ENT_TYPE_DRAINAGE, 
                "pain":ENTHistory.ENT_TYPE_PAIN,
                "other":ENTHistory.ENT_TYPE_OTHER}
        try:
            ret = data[val]
        except:
            pass
        return ret

    def durationToString(self, val):
        ret = None 
        data = {ENTHistory.EAR_DURATION_NONE:"none",
                ENTHistory.EAR_DURATION_DAYS:"days",
                ENTHistory.EAR_DURATION_WEEKS:"weeks",
                ENTHistory.EAR_DURATION_MONTHS:"months",
                ENTHistory.EAR_DURATION_INTERMITTENT:"intermittent"}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def stringToDuration(self, val):
        ret = None 
        data = {"none":ENTHistory.EAR_DURATION_NONE,
                "days":ENTHistory.EAR_DURATION_DAYS,
                "weeks":ENTHistory.EAR_DURATION_WEEKS,
                "months":ENTHistory.EAR_DURATION_MONTHS,
                "intermittent":ENTHistory.EAR_DURATION_INTERMITTENT}

        try:
            ret = data[val]
        except:
            pass
        return ret

    def sideToString(self, val):
        ret = None 
        data = {ENTHistory.EAR_SIDE_LEFT:"left",
                ENTHistory.EAR_SIDE_RIGHT:"right",
                ENTHistory.EAR_SIDE_BOTH:"both"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToSide(self, val):
        ret = None 
        data = {"left":ENTHistory.EAR_SIDE_LEFT,
                "right":ENTHistory.EAR_SIDE_RIGHT,
                "both":ENTHistory.EAR_SIDE_BOTH}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["username"] = entry.username
        m["time"] = entry.time
        m["type"] = self.ENTTypeToString(entry.type)
        m["name"] = entry.name
        m["duration"] = self.durationToString(entry.duration)
        m["side"] = self.sideToString(entry.side)
        m["comment"] = entry.comment 

        return m

    @log_request
    def get(self, request, ent_history_id=None, format=None):
        ent_history = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if ent_history_id:
            try:
                ent_history = ENTHistory.objects.get(id = ent_history_id)
            except:
                ent_history = None
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
                val = request.GET.get('type', '')
                if val != '':
                    val = self.stringToENTType(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["type"] = val
                        if val == ENT_TYPE_OTHER:
                            # name is required if type is "other"
                            try:
                                val = request.GET.get('name', '')
                                kwargs["name"] = val
                            except:
                                badRequest = True
            except:
                pass

            try:
                val = request.GET.get('duration', '')
                if val != '':
                    val = self.stringToDuration(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["duration"] = val
            except:
                pass

            try:
                val = request.GET.get('side', '')
                if val != '':
                    val = self.stringToSide(val)
                    if val == None:
                        badRequest = True
                    else:
                        kwargs["side"] = val
            except:
                pass

            if not badRequest:
                try:
                    ent_history = ENTHistory.objects.filter(**kwargs)
                except:
                    ent_history = None

        if not ent_history and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_history_id:
                ret = self.serialize(ent_history)
            else:
                ret = []
                for x in ent_history:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "username" in data:
            valid = False
        elif len(data["username"]) == 0:
            valid = False

        try:
            val = self.stringToENTType(data["type"])
            if val == None:
                valid = False
            else:
                kwargs["type"] = val
        except:
            valid = False

        try:
            val = self.stringToDuration(data["duration"])
            if val == None:
                valid = False
            else:
                kwargs["duration"] = val
        except:
            valid = False

        try:
            val = self.stringToSide(data["side"])
            if val == None:
                valid = False
            else:
                kwargs["side"] = val
        except:
            valid = False

        return valid, kwargs

    def validatePutArgs(self, data, ent_history):
        valid = True

        try:
            if "type" in data:
                val = self.stringToENTType(data["type"])
                if val == None:
                    valid = False
                else:
                    ent_history.type = val
                    if val == ENTHistory.ENT_TYPE_OTHER:
                        if not "name" in data:
                            valid = False
                        elif len(data["name"]) == 0:
                            valid = False
                        else:
                            ent_history.name = data["name"]
        except:
            pass

        try:
            if "duration" in data:
                val = self.stringToDuration(data["duration"])
                if val == None:
                    valid = False
                else:
                    ent_history.duration = val
        except:
            pass

        try:
            if "side" in data:
                val = self.stringToSide(data["side"])
                if val == None:
                    valid = False
                else:
                    ent_history.side = val
        except:
            pass

        try:
            if "clinic" in data:
                aClinic = Clinic.objects.get(id=int(data["clinic"]))
                ent_history.clinic = data["clinic"]
        except:
            pass

        try:
            if "patient" in data:
                aPatient = Patient.objects.get(id=int(data["patient"]))
                ent_history.patient = aPatient
        except:
            pass

        try:
            if "comment" in data:
                ent_history.comment = data["comment"]
        except:
            pass

        val = "type" in data or "name" in data or "duration" in data or "side" in data or "comment" in data or "username" in data
        if val == False:
            valid = False

        return valid, ent_history

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
                ent_history = ENTHistory(**kwargs)
                if ent_history:
                    ent_history.save()
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
            return Response({'id': ent_history.id})

    @log_request
    def put(self, request, ent_history_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_history_id:
            badRequest = True

        if not badRequest:
            ent_history = None

            try:
                ent_history = ENTHistory.objects.get(id=ent_history_id)
            except:
                pass

            if not ent_history:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_history = self.validatePutArgs(data, ent_history)
                    if valid: 
                        ent_history.save()
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
    def delete(self, request, ent_history_id=None, format=None):
        ent_history = None

        # see if the state change object exists

        if not ent_history_id:
            return HttpResponseBadRequest()
        try:
            ent_history = ENTHistory.objects.get(id=ent_history_id)
        except:
            ent_history = None

        if not ent_history:
            raise NotFound
        else:
            ent_history.delete()

        return Response({})
