#(C) Copyright Syd Logan 2018
#(C) Copyright Thousand Smiles Foundation 2018
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
from returntoclinicstation.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import numbers

from common.decorators import *

import json
import sys

class ReturnToClinicStationView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def stateToDb(self, state):
        ret = None

        if state == "created":
            ret = '1' 
        elif state == "scheduled_dest":
            ret = '2'
        elif state == "checked_out_dest":
            ret = '3'
        elif state == "scheduled_return":
            ret = '4'
        return ret

    def dbToState(self, db):
        ret = None

        if db == '1':
            ret = "created"
        elif db == '2':
            ret = "scheduled_dest"
        elif db == '3':
            ret = "checked_out_dest"
        elif db == '4':
            ret = "scheduled_return"
        return ret

    @log_request
    def get(self, request, returntoclinicstation_id=None, format=None):
        notFound = False
        badRequest = False
        returntoclinicstation = None
        if returntoclinicstation_id:
            try:
                returntoclinicstation = ReturnToClinicStation.objects.get(id = returntoclinicstation_id)
            except:
                returntoclinicstation = None
        else:
            kwargs = {}
            try:
                clinicid = request.GET.get('clinic', '')
                if clinicid != '':
                    clinicid = int(clinicid)
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        kwargs["clinic"] = aClinic
                    except:
                        notFound = True
            except:
                pass

            try:
                patientid = request.GET.get('patient', '')
                if patientid != '':
                    patientid = int(patientid)
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        kwargs["patient"] = aPatient
                    except:
                        notFound = True
            except:
                pass

            try:
                clinicstationid = request.GET.get('clinicstation', '')
                if clinicstationid != '':
                    clinicstationid = int(clinicstationid)
                    try:
                        aClinicStation = ClinicStation.objects.get(id=clinicstationid)
                        kwargs["clinicstation"] = aClinicStation
                    except:
                        notFound = True
            except:
                pass

            try:
                requestingclinicstationid = request.GET.get('requestingclinicstation', '')
                if requestingclinicstationid != '':
                    requestingclinicstationid = int(requestingclinicstationid)
                    try:
                        aRequestingClinicStation = ClinicStation.objects.get(id=requestingclinicstationid)
                        kwargs["requestingclinicstation"] = aRequestingClinicStation
                    except:
                        notFound = True
            except:
                pass

            try:
                state = request.GET.get('state', '')
                if state != '':
                    stateDb = self.stateToDb(state)
                    if stateDb == None:
                        badRequest = True
                    else:
                        kwargs["state"] = stateDb
            except:
                pass

            if (not badRequest) and (not notFound) and (len(kwargs) == 0):
                returntoclinicstation = ReturnToClinicStation.objects.all()
            elif not badRequest and not notFound:
                try:
                    returntoclinicstation = ReturnToClinicStation.objects.filter(**kwargs)
                except:
                    returntoclinicstation = None

        if notFound or not returntoclinicstation:
            raise NotFound
        elif badRequest:
            raise BadRequest
        elif returntoclinicstation_id: 
            ret = {}
            x = returntoclinicstation
            ret["clinic"] = x.clinic.id  
            ret["patient"] = x.patient.id  
            ret["clinicstation"] = x.clinicstation.id  
            ret["requestingclinicstation"] = x.requestingclinicstation.id  
            ret["createtime"] = x.createtime  
            ret["statechangetime"] = x.statechangetime  
            ret["state"] = self.dbToState(x.state)
            ret["id"] = x.id
        else:
            ret = []
            for x in returntoclinicstation:
                m = {}
                m["id"] = x.id
                ret.append(m)
        return Response(ret)

    @log_request
    def put(self, request, id=None, format=None):
        badRequest = False
        implError = False
        notFound = False
        state = None

        data = json.loads(request.body)
        try:
            state = data["state"]
        except:
            pass

        if state == None:  
            badRequest = True

        stateDb = self.stateToDb(state)

        if stateDb == None:
            badRequest = True

        if not badRequest:
            returntoclinicstation = None

            # see if the returntoclinicstation already exists

            try:
                returntoclinicstation = ReturnToClinicStation.objects.get(id=id)
            except:
                pass

            if not returntoclinicstation:
                notFound = True 
            else:
                try:
                    returntoclinicstation.state=stateDb
                    returntoclinicstation.save()
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
    def post(self, request, format=None):
        badRequest = False
        notFound = False
        implError = False
        aClinic = None
        aPatient = None
        aClinicStation = None
        aRequestingClinicStation = None
        state = None 

        data = json.loads(request.body)
        try:
            clinic = data["clinic"]
        except:
            badRequest = True
        try:
            patient = data["patient"]
        except:
            badRequest = True
        try:
            clinicstation = data["clinicstation"]
        except:
            badRequest = True
        try:
            requestingclinicstation = data["requestingclinicstation"]
        except:
            badRequest = True

        if not badRequest:
            try:
                aClinic = Clinic.objects.get(id=clinic)
            except:
                aClinic = None

            try:
                aClinicStation = ClinicStation.objects.get(id=clinicstation)
            except:
                aClinicStation = None

            try:
                aRequestingClinicStation = ClinicStation.objects.get(id=requestingclinicstation)
            except:
                aRequestingClinicStation = None

            try:
                aPatient = Patient.objects.get(id=patient)
            except:
                aPatient = None

            if not aClinic or not aClinicStation or not aPatient or not aRequestingClinicStation:
                notFound = True

        if not badRequest and not notFound:

            returntoclinicstation = None

            # see if the returntoclinicstation already exists

            try:
                returntoclinicstation = ReturnToClinicStation.objects.filter(clinic=aClinic,
                                                 patient=aPatient,
                                                 clinicstation=aClinicStation,
                                                 requestingclinicstation=aRequestingClinicStation)
                if not returntoclinicstation or len(returntoclinicstation) == 0:
                    returntoclinicstation = None
            except:
                implMsg = "ReturnToClinicStation.objects.filter {} {}".format(sys.exc_info()[0], data)
                implError = True

            if not returntoclinicstation:
                try:
                    returntoclinicstation = ReturnToClinicStation(clinic=aClinic,
                                      patient=aPatient,
                                      clinicstation=aClinicStation,
                                      requestingclinicstation=aRequestingClinicStation,
                                      state='1')
                    if returntoclinicstation:
                        returntoclinicstation.save()
                    else:
                        implMsg = "Unable to create returntoclinicstation"
                        implError = True
                except:
                    implMsg = "ReturnToClinicStation create {} {}".format(sys.exc_info()[0], data)
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': returntoclinicstation.id})
       
    @log_request 
    def delete(self, request, returntoclinicstation_id=None, format=None):
        returntoclinicstation = None

        # see if the returntoclinicstation resource exists

        try:
            returntoclinicstation = ReturnToClinicStation.objects.get(id=returntoclinicstation_id)
        except:
            returntoclinicstation = None

        if not returntoclinicstation:
            raise NotFound
        else:
            returntoclinicstation.delete()

        return Response({})
