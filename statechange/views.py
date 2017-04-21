#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2017
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
from statechange.models import *
from clinicstation.models import *
from patient.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import sys

import json

class StateChangeView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinicstation"] = entry.clinicstation_id
        m["patient"] = entry.patient_id
        m["time"] = entry.time
        if entry.state == 'i':
            m["state"] = "in"
        else:
            m["state"] = "out"

        return m

    def get(self, request, state_change_id=None, format=None):
        state_change = None
        badRequest = False
        aPatient = None
        aClinic = None
        aStation = None
        aClinicStation = None
        kwargs = {}

        if state_change_id:
            try:
                state_change = StateChange.objects.get(id = state_change_id)
            except:
                state_change = None
        else:
            # look for optional arguments
            data = json.loads(request.body)
            try:
                patientid = int(data["patient"])
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
                clinicid = int(data["clinic"])
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                    if not aClinic:
                        badRequest = True
                    else:
                        kwargs["clinic"] = aPatient
                except:
                    badRequest = True
            except:
                pass # no clinic ID

            try:
                clinicstationid = int(data["clinicstation"])
                try:
                    aClinicStation = ClinicStation.objects.get(id=clinicstationid)
                    if not aClinicStation:
                        badRequest = True
                    else:
                        kwargs["clinicstation"] = aClinicStation
                except:
                    badRequest = True
            except:
                pass # no clinicstation ID

            if not badRequest and len(kwargs):
                # look for invalid arg combinations

                # there are 4 legal combination of args

                case1 = False
                case2 = False
                case3 = False
                case4 = False

                if aPatient and aClinicStation and not aClinic:
                    case1 = True
                elif aPatient and aClinic and not aClinicStation:
                    case2 = True
                elif aClinicStation and not aClinic and not aPatient:
                    case3 = True
                elif aClinic and not aClinicStation and not aPatient:
                    case4 = True
                else:
                    badRequest = True

            if not badRequest and (case1 or case3):
                kwargs = {}
                if case1:
                    kwargs["patient"] = aPatient;
                    kwargs["clinicstation"] = aClinicStation
                elif case3:
                    kwargs["clinicstation"] = aClinicStation
                try:
                    state_change = StateChange.objects.filter(**kwargs)
                except:
                    state_change = None
            elif not badRequest and case2:
                # get all clinicstations for the clinic. 
                # state_change = []
                # for each clinicstation:
                #    get statechanges for patient, clinicstation
                #    append these to state_change

                clinicstations = ClinicStation.objects.filter(clinic=aClinic);
                state_change = []
           
                kwargs = {}
                kwargs["patient"] = aPatient 
                for x in clinicstations:
                    kwargs["clinicstation"] = x 
                    y = StateChange.objects.filter(**kwargs)
                    for el in y:
                        state_change.append(el)
            elif not badRequest and case4:      
                # get all clinicstations for the clinic. 
                # state_change = []
                # for each clinicstation:
                #    get statechanges for clinicstation
                #    append these to state_change

                clinicstations = ClinicStation.objects.filter(clinic=aClinic);
                state_change = []
           
                kwargs = {}
                for x in clinicstations:
                    kwargs["clinicstation"] = x 
                    y = StateChange.objects.filter(**kwargs)
                    for el in y:
                        state_change.append(el)

        if not state_change and not badRequest:
            raise NotFound
        elif not badRequest:
            if state_change_id:
                ret = self.serialize(state_change)
            else:
                ret = []
                for x in state_change:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            clinicstationid = int(data["clinicstation"])
        except:
            badRequest = True

        try:
            state = data["state"]
            if not state in ["in", "out"]:
                badRequest = True
            else:
                if state == "in":
                    state = "i"
                else:
                    state = "o"
        except:
            badRequest = True

        if not badRequest:

            # get the instances

            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None
 
            try:
                aClinicStation = ClinicStation.objects.get(id=clinicstationid)
            except:
                aClinicStation = None

            if not aPatient or not aClinicStation:
                raise NotFound

        if not badRequest:
                
            try:
                state_change = StateChange(patient=aPatient, clinicstation=aClinicStation, state=state)
                if state_change:
                    state_change.save()
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
            return Response({'id': state_change.id})

    def delete(self, request, state_change_id=None, format=None):
        state_change = None

        # see if the state change object exists

        if not state_change_id:
            return HttpResponseBadRequest()
        try:
            state_change = StateChange.objects.filter(id=state_change_id)
            if not state_change or len(state_change) == 0:
                state_change = None
            else:
                state_change = state_change[0]
        except:
            state_change = None

        if not state_change:
            raise NotFound
        else:
            state_change.delete()

        return Response({})
