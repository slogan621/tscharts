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
from entsurgicalhistory.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

class ENTSurgicalHistoryView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    sideKeyNames = ["tubes", "tplasty", "eua", "fb", "myringotomy", "cerumen", "granuloma"]
    booleanKeyNames = ["septorhinoplasty", "scarrevision", "frenulectomy"]

    def sideToString(self, val):
        ret = None 
        data = {ENTSurgicalHistory.EAR_SIDE_LEFT:"left",
                ENTSurgicalHistory.EAR_SIDE_RIGHT:"right",
                ENTSurgicalHistory.EAR_SIDE_BOTH:"both",
                ENTSurgicalHistory.EAR_SIDE_NONE:"none"}

        try:
            ret = data[val]
        except:
            pass
        return ret    

    def stringToSide(self, val):
        ret = None 
        data = {"left":ENTSurgicalHistory.EAR_SIDE_LEFT,
                "right":ENTSurgicalHistory.EAR_SIDE_RIGHT,
                "both":ENTSurgicalHistory.EAR_SIDE_BOTH,
                "none":ENTSurgicalHistory.EAR_SIDE_NONE}

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

        m["tubes"] = self.sideToString(entry.tubes)
        m["tubescomment"] = entry.tubescomment
        m["tplasty"] = self.sideToString(entry.tplasty)
        m["tplastycomment"] = entry.tplastycomment
        m["eua"] = self.sideToString(entry.eua)
        m["euacomment"] = entry.euacomment
        m["fb"] = self.sideToString(entry.fb)
        m["fbcomment"] = entry.fbcomment
        m["myringotomy"] = self.sideToString(entry.myringotomy)
        m["myringotomycomment"] = entry.myringotomycomment
        m["cerumen"] = self.sideToString(entry.cerumen)
        m["cerumencomment"] = entry.cerumencomment
        m["septorhinoplasty"] = entry.septorhinoplasty
        m["septorhinoplastycomment"] = entry.septorhinoplastycomment
        m["scarrevision"] = entry.scarrevision
        m["scarrevisioncomment"] = entry.scarrevisioncomment
        m["frenulectomy"] = entry.frenulectomy
        m["frenulectomycomment"] = entry.frenulectomycomment
        return m

    @log_request
    def get(self, request, ent_surgicalhistory_id=None, format=None):
        ent_surgicalhistory = None
        badRequest = False
        aPatient = None
        aClinic = None
        kwargs = {}

        if ent_surgicalhistory_id:
            try:
                ent_surgicalhistory = ENTSurgicalHistory.objects.get(id = ent_surgicalhistory_id)
            except:
                ent_surgicalhistory = None
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

            if not badRequest:
                try:
                    ent_surgicalhistory = ENTSurgicalHistory.objects.filter(**kwargs)
                except:
                    ent_surgicalhistory = None

        if not ent_surgicalhistory and not badRequest:
            raise NotFound
        elif not badRequest:
            if ent_surgicalhistory_id:
                ret = self.serialize(ent_surgicalhistory)
            else:
                ret = []
                for x in ent_surgicalhistory:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        if not "clinic" in data:
            valid = False

        if not "patient" in data:
            valid = False

        if not "username" in data:
            valid = False
        elif len(data["username"]) == 0:
            valid = False
        
        for x in self.sideKeyNames:
            if not x in data:
                valid = False
                break
            try:
                val = self.stringToSide(data[x])
                if val == None:
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                valid = False
                break

        for x in self.booleanKeyNames:
            if not x in data:
                valid = False
                break
            try:
                val = data[x]
                if not val in [True, False]:
                    valid = False
                    break
                else:
                    kwargs[x] = val
            except:
                valid = False
                break

        return valid, kwargs

    def validatePutArgs(self, data, ent_surgicalhistory):
        valid = True
        foundOne = False

        if "username" in data:
            if len(data["username"]) == 0:
                valid = False
            else:
                ent_surgicalhistory.username = data["username"]
                foundOne = True
        
        for x in self.sideKeyNames:
            if not x in data:
                continue
            try:
                val = self.stringToSide(data[x])
                if val == None:
                    valid = False
                    break
                else:
                    if x == "tubes":
                        ent_surgicalhistory.tubes = val
                        foundOne = True
                    elif x == "tplasty":
                        ent_surgicalhistory.tplasty = val
                        foundOne = True
                    elif x == "eua":
                        ent_surgicalhistory.eua = val
                        foundOne = True
                    elif x == "fb":
                        ent_surgicalhistory.fb = val
                        foundOne = True
                    elif x == "myringotomy":
                        ent_surgicalhistory.myringotomy = val
                        foundOne = True
                    elif x == "cerumen":
                        ent_surgicalhistory.cerumen = val
                        foundOne = True
                    elif x == "granuloma":
                        ent_surgicalhistory.granuloma = val
                        foundOne = True
            except:
                valid = False
                break

        for x in self.booleanKeyNames:
            if not x in data:
                continue
            try:
                val = data[x]
                if val == None:
                    valid = False
                    break
                elif not val in [True, False]:
                    valid = False
                    break
                    
                if x == "septorhinoplasty":
                    ent_surgicalhistory.septorhinoplasty = val
                    foundOne = True
                elif x == "scarrevision":
                    ent_surgicalhistory.scarrevision = val
                    foundOne = True
                elif x == "frenulectomy":
                    ent_surgicalhistory.frenulectomy = val
                    foundOne = True
            except:
                valid = False
                break

        if foundOne == False:
            valid = False

        return valid, ent_surgicalhistory

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
                ent_surgicalhistory = ENTSurgicalHistory(**kwargs)
                if ent_surgicalhistory:
                    ent_surgicalhistory.save()
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
            return Response({'id': ent_surgicalhistory.id})

    @log_request
    def put(self, request, ent_surgicalhistory_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not ent_surgicalhistory_id:
            badRequest = True

        if not badRequest:
            ent_surgicalhistory = None

            try:
                ent_surgicalhistory = ENTSurgicalHistory.objects.get(id=ent_surgicalhistory_id)
            except:
                pass

            if not ent_surgicalhistory:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, ent_surgicalhistory = self.validatePutArgs(data, ent_surgicalhistory)
                    if valid: 
                        ent_surgicalhistory.save()
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
    def delete(self, request, ent_surgicalhistory_id=None, format=None):
        ent_surgicalhistory = None

        # see if the ent surgical history object exists

        if not ent_surgicalhistory_id:
            return HttpResponseBadRequest()
        try:
            ent_surgicalhistory = ENTSurgicalHistory.objects.get(id=ent_surgicalhistory_id)
        except:
            ent_surgicalhistory = None

        if not ent_surgicalhistory:
            raise NotFound
        else:
            ent_surgicalhistory.delete()

        return Response({})
