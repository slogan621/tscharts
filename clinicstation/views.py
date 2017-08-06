#(C) Copyright Syd Logan 2016
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
from clinicstation.models import *
from station.models import *
from clinic.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

class ClinicStationView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, clinic_station_id=None, format=None):
        clinic_station = None
        badRequest = False
        notFound = False
        aClinic = None

        if clinic_station_id:
            try:
                clinic_station = ClinicStation.objects.get(id = clinic_station_id)
            except:
                clinic_station = None
        else:
            kwargs = {}
            clinicid = request.GET.get('clinic', '')
            if clinicid == '':
                badRequest = True
            else:
                try:
                    clinicid = int(clinicid)
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        kwargs["clinic"] = aClinic
                    except:
                        notFound = True
                except:
                    badRequest = True

            if not badRequest and not notFound:
                active = request.GET.get('active', '')
                if active != '':
                    if not active in [True, False]:
                        badRequest = True
                    else:
                        kwargs["active"] = active
                level = request.GET.get('level', '')
                if level != '':
                    kwargs["level"] = int(level)
                away = request.GET.get('away', '')
                if away != '':
                    if not away in [True, False]:
                        badRequest = True
                    else:
                        kwargs["away"] = away

            if not badRequest and not notFound:
                try:
                    clinic_station = ClinicStation.objects.filter(**kwargs)
                except:
                    clinic_station = None
                    notFound = True

        if badRequest:
            return HttpResponseBadRequest()
        elif notFound or not clinic_station:
            return HttpResponseNotFound()
        else:
            if clinic_station_id:
                m = {}
                m["id"] = clinic_station.id  
                m["name"] = clinic_station.name
                m["name_es"] = clinic_station.name_es
                m["clinic"] = clinic_station.clinic_id
                m["station"] = clinic_station.station_id
                m["active"] = clinic_station.active
                m["level"] = clinic_station.level
                m["away"] = clinic_station.away
                m["awaytime"] = clinic_station.awaytime
                m["willreturn"] = clinic_station.willreturn
                m["activepatient"] = clinic_station.activepatient_id
                m["nextpatient"] = clinic_station.nextpatient_id
                ret = m
            else: 
                ret = []
                for x in clinic_station:
                    m = {}
                    m["id"] = x.id  
                    m["name"] = x.name
                    m["name_es"] = x.name_es
                    m["clinic"] = x.clinic_id
                    m["station"] = x.station_id
                    m["active"] = x.active
                    m["level"] = x.level
                    m["away"] = x.away
                    m["awaytime"] = x.awaytime
                    m["willreturn"] = x.willreturn
                    m["activepatient"] = x.activepatient_id
                    m["nextpatient"] = x.nextpatient_id
                    ret.append(m)
            return Response(ret)

    def post(self, request, format=None):
        badRequest = False
        implError = False

        kwargs = {}

        data = json.loads(request.body)
        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True

        try:
            stationid = int(data["station"])
        except:
            badRequest = True

        try:
            kwargs["name"] = data["name"]
        except:
            badRequest = True

        try:
            kwargs["name_es"] = data["name_es"]
        except:
            badRequest = True

        if "active" in data:
            active = data["active"]
            if not active == True and not active == False:
                badRequest = True
            else:
                kwargs["active"] = active
                if active == False:
                    kwargs["activepatient"] = None

        if "away" in data:
            away = data["away"]
            if not away == True and not away == False:
                badRequest = True
            else:
                kwargs["away"] = away

        if "level" in data:
            kwargs["level"] = data["level"]

        if "activepatient" in data:
            kwargs["activepatient"] = data["activepatient"]

        if "nextpatient" in data:
            kwargs["nextpatient"] = data["nextpatient"]

        if "awaytime" in data:
            awaytime = data["awaytime"]
        else:
            awaytime = 30

        kwargs["awaytime"] = awaytime
        kwargs["willreturn"] = datetime.now() + timedelta(minutes=awaytime)

        if not badRequest:

            # get the station and clinic instances

            try:
                aStation = Station.objects.get(id=stationid)
            except:
                aStation = None
 
            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None

            if not aStation or not aClinic:
                raise NotFound
            else:
                kwargs["station"] = aStation   
                kwargs["clinic"] = aClinic   

        if not badRequest:
 
            clinic_station = None

            # see if the station already exists

            try:
                clinic_station = ClinicStation.objects.filter(clinic=aClinic,
                                                              station=aStation,
                                                              name=name)
                if not clinic_station or len(clinic_station) == 0:
                    clinic_station = None
                else:
                    clinic_station = clinic_station[0]
            except:
                pass

            if not clinic_station:
                try:
                    clinic_station = ClinicStation(**kwargs)
                    if clinic_station:
                        clinic_station.save()
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
            return Response({'id': clinic_station.id})

    def put(self, request, clinic_station_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False
        active = None
        level = None
        name = None
        name_es = None
        away = None
        awaytime = None
        activepatient = None
        nextpatient = None
        hasActivePatient = False
        hasNextPatient = False

        data = json.loads(request.body)

        if "active" in data:
            active = data["active"]
            if not active == True and not active == False:
                badRequest = True
        if "away" in data:
            away = data["away"]
            if not away == True and not away == False:
                badRequest = True
        if "level" in data:
            level = data["level"]
        if "awaytime" in data:
            awaytime = data["awaytime"]
        if "name" in data:
            name = data["name"]
        if "name_es" in data:
            name_es = data["name_es"]

        if "activepatient" in data:
            activepatient = data["activepatient"]
            hasActivePatient = True

        if "nextpatient" in data:
            nextpatient = data["nextpatient"]
            hasNextPatient = True

        if level == None and away == None and active == None and awaytime == None and name == None and name_es == None and hasActivePatient == False and hasNextPatient == False:
            badRequest = True   # update but no data provided

        if not badRequest:
            clinic_station = None

            # see if the clinic station already exists

            try:
                clinic_station = ClinicStation.objects.get(id=clinic_station_id)
            except:
                pass

            if not clinic_station:
                notFound = True 

            if notFound == False and hasActivePatient and (not activepatient == None):
                try:
                    activepatient = Patient.objects.get(id=activepatient)
                except:
                    pass

                if not activepatient:
                    notFound = True 

            if notFound == False and hasNextPatient and (not nextpatient == None):
                try:
                    nextpatient = Patient.objects.get(id=nextpatient)
                except:
                    pass

                if not nextpatient:
                    notFound = True 

            if notFound == False:
                try:
                    if not (awaytime == None):
                        clinic_station.awaytime = awaytime
                    if not (away == None):
                        clinic_station.away = away
                        if away == True:
                            clinic_station.willreturn = datetime.now() + timedelta(minutes=clinic_station.awaytime)
                    if not (active == None):
                        clinic_station.active=active
                    if not (level == None):
                        clinic_station.level=level
                    if not (name == None):
                        clinic_station.name=name
                    if not (name_es == None):
                        clinic_station.name_es=name_es
                    if hasActivePatient:
                        clinic_station.activepatient_id = activepatient
                    if hasNextPatient:
                        clinic_station.nextpatient_id = nextpatient
                    clinic_station.save()
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
        
    def delete(self, request, clinic_station_id=None, format=None):
        clinic_station = None

        # see if the station exists

        if not clinic_station_id:
            return HttpResponseBadRequest()
        try:
            clinic_station = ClinicStation.objects.filter(id=clinic_station_id)
            if not clinic_station or len(clinic_station) == 0:
                clinic_station = None
            else:
                clinic_station = clinic_station[0]
        except:
            clinic_station = None

        if not clinic_station:
            raise NotFound
        else:
            clinic_station.delete()

        return Response({})
