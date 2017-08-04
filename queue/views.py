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
from station.models import *
from clinic.models import *
from clinicstation.models import *
from queue.models import *
from datetime import *
import sys
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json

class QueueView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):

        super(QueueView, self).__init__()

    def get(self, request, format=None):
        badRequest = False
        notFound = False
        aClinic = None
        aStation = None
        queues = None
        queueStatus = None
        internalError = False
        ret = {}

        clinicid = request.GET.get('clinic', '')
        stationid = request.GET.get('station', '')
        clinicstation = request.GET.get('clinicstation', '')
        if not clinicid == '':
            try:
                clinicid = int(clinicid)
                try:
                    aClinic = Clinic.objects.get(id=clinicid)
                except:
                    aClinic = None
                    notFound = True
            except:
                badRequest = True
        else:
            badRequest = True # required arg

        if not stationid == '':
            try:
                stationid = int(stationid)
                try:
                    aStation = Station.objects.get(id=stationid)
                except:
                    aStation = None
                    notFound = True
            except:
                pass

        if not notFound and not badRequest:
            kwargs = {}
            kwargs["clinic"] = aClinic
            if aStation:
                kwargs["station"] = aStation 
            try:
                queues = Queue.objects.filter(**kwargs)
                if not queues or len(queues) == 0:
                    notFound = True
            except:
                notFound = True

        if not notFound and not badRequest:
            try:
                queueStatus = QueueStatus.objects.filter(clinic=aClinic)
                if not queueStatus or len(queueStatus) == 0:
                    notFound = True
                elif queueStatus and len(queueStatus) > 1:
                    internalError = True
                else:
                    queueStatus = queueStatus[0]
            except:
                internalError = True

        if not notFound and not badRequest and not internalError:
            ret["status"] = {"numwaiting": queueStatus.numwaiting,
                             "minq": queueStatus.minq,
                             "maxq": queueStatus.maxq,
                             "avgq": queueStatus.avgq,
                             "minwait": queueStatus.minwait,
                             "maxwait": queueStatus.maxwait,
                             "avgwait": queueStatus.avgwait}
            ret["queues"] = []
            for x in queues:
                if not clinicstation == '' and int(clinicstation) != x.clinicstation_id:
                    # clinicstation does not match
                    continue
                queueData = {}
                aClinicStation = None
                try:
                    aClinicStation = ClinicStation.objects.get(id=x.clinicstation_id)
                except:
                    aClinicStation = None

                if not aClinicStation:
                    internalError = True
                    break

                queueData["name"] = aClinicStation.name
                queueData["name_es"] = aClinicStation.name_es
                queueData["clinicstation"] = aClinicStation.id
                queueData["avgservicetime"] = x.avgservicetime
                queueData["entries"] = []

                try:
                    queueEntries = QueueEntry.objects.filter(queue=x.id)
                    if not queueEntries:
                        queueEntries = []
                except:
                    internalError = True

                if internalError:
                    break

                for y in queueEntries: 
                    entryData = {}
                    entryData["patient"] = y.patient_id
                    entryData["timein"] = str(y.timein)
                    entryData["waittime"] = str(y.waittime)
                    entryData["estwaittime"] = str(y.estwaittime)
                    entryData["routingslipentry"] = y.routingslipentry_id
                    
                    queueData["entries"].append(entryData)
               
                ret["queues"].append(queueData) 
 
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if internalError:
            return HttpResponseServerError()
        return Response(ret)
