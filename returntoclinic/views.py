#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2016
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
from returntoclinic.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import numbers

from common.decorators import *

import json
import sys

class ReturnToClinicView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @log_request
    def get(self, request, returntoclinic_id=None, format=None):
        notFound = False
        returntoclinic = None
        if returntoclinic_id:
            try:
                returntoclinic = ReturnToClinic.objects.get(id = returntoclinic_id)
            except:
                returntoclinic = None
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
                stationid = request.GET.get('station', '')
                if stationid != '':
                    stationid = int(stationid)
                    try:
                        aStation = Station.objects.get(id=stationid)
                        kwargs["station"] = aStation
                    except:
                        notFound = True
            except:
                pass

            try:
                returntoclinic = ReturnToClinic.objects.filter(**kwargs)
            except:
                returntoclinic = None

        if notFound or not returntoclinic:
            raise NotFound
        elif returntoclinic_id: 
            ret = {}
            x = returntoclinic
            ret["clinic"] = x.clinic.id  
            ret["station"] = x.station.id  
            ret["patient"] = x.patient.id  
            ret["comment"] = x.comment  
            ret["interval"] = x.interval  
            ret["month"] = (x.clinic.start + timedelta(x.interval * 365/12)).month
            ret["year"] = (x.clinic.start + timedelta(x.interval * 365/12)).year
            ret["id"] = x.id
        else:
            ret = []
            for x in returntoclinic:
                m = {}
                m["id"] = x.id
                ret.append(m)
        return Response(ret)

    @log_request
    def put(self, request, id=None, format=None):
        badRequest = False
        implError = False
        notFound = False
        interval = None
        comment = None

        data = json.loads(request.body)
        try:
            interval = data["interval"]
        except:
            pass
        try:
            comment = data["comment"]
        except:
            pass

        if interval == None and comment == None:
            badRequest = True

        if not interval == None and not isinstance(interval, numbers.Number):
            badRequest = True

        if not badRequest:
            returntoclinic = None

            # see if the returntoclinic already exists

            try:
                returntoclinic = ReturnToClinic.objects.get(id=id)
            except:
                pass

            if not returntoclinic:
                notFound = True 
            else:
                try:
                    if interval != None:
                        returntoclinic.interval=interval
                    if comment != None:
                        returntoclinic.comment=comment
                    returntoclinic.save()
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
        aStation = None
        interval = None 

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
            station = data["station"]
        except:
            badRequest = True
        try:
            interval = data["interval"]
        except:
            badRequest = True
        try:
            comment = data["comment"]
        except:
            badRequest = True

        if not badRequest:
            try:
                aClinic = Clinic.objects.get(id=clinic)
            except:
                aClinic = None

            try:
                aStation = Station.objects.get(id=station)
            except:
                aStation = None

            try:
                aPatient = Patient.objects.get(id=patient)
            except:
                aPatient = None

            if not interval:
                badRequest = True

            if not isinstance(interval, numbers.Number):
                badRequest = True

            if not aClinic or not aStation or not aPatient:
                notFound = True

        if not badRequest and not notFound:

            returntoclinic = None

            # see if the returntoclinic already exists

            try:
                returntoclinic = ReturnToClinic.objects.filter(clinic=aClinic,
                                                 patient=aPatient,
                                                 station=aStation)
                if not returntoclinic or len(returntoclinic) == 0:
                    returntoclinic = None
                else:
                    returntoclinic = returntoclinic[0]
                    if returntoclinic:
                        returntoclinic.interval = interval
                        returntoclinic.comment = comment
                        returntoclinic.save()
            except:
                implMsg = "ReturnToClinic.objects.filter {} {}".format(sys.exc_info()[0], data)
                implError = True

            if not returntoclinic:
                try:
                    returntoclinic = ReturnToClinic(clinic=aClinic,
                                      patient=aPatient,
                                      station=aStation,
                                      comment=comment,
                                      interval=interval)
                    if returntoclinic:
                        returntoclinic.save()
                    else:
                        implMsg = "Unable to create returntoclinic"
                        implError = True
                except:
                    implMsg = "ReturnToClinic create {} {}".format(sys.exc_info()[0], data)
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': returntoclinic.id})
       
    @log_request 
    def delete(self, request, returntoclinic_id=None, format=None):
        returntoclinic = None

        # see if the returntoclinic exists

        try:
            returntoclinic = ReturnToClinic.objects.get(id=returntoclinic_id)
        except:
            returntoclinic = None

        if not returntoclinic:
            raise NotFound
        else:
            returntoclinic.delete()

        return Response({})
