#(C) Copyright Syd Logan 2016-2018
#(C) Copyright Thousand Smiles Foundation 2016-2018
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
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json

class StationView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, station_id=None, format=None):
        station = None
        if station_id:
            try:
                station = Station.objects.get(id = station_id)
            except:
                station = None
        else:
            try:
                station = Station.objects.all()
            except:
                station = None

        if not station:
            raise NotFound
        else:
            if station_id:
                m = {}
                m["id"] = station.id  
                m["name"] = station.name
                m["level"] = station.level
                ret = m
            else:
                ret = []
                for x in station:
                    m = {}
                    m["id"] = x.id  
                    m["name"] = x.name
                    m["level"] = x.level
                    ret.append(m)
            return Response(ret)

    def post(self, request, format=None):
        badRequest = False
        implError = False

        kwargs = {}

        data = json.loads(request.body)
        try:
            kwargs["name"] = data["name"]
            name = kwargs["name"]
        except:
            badRequest = True
        try:
            kwargs["level"] = data["level"]
        except:
            pass

        if not badRequest:
            station = None

            # see if the station already exists

            try:
                station = Station.objects.filter(name=name)
                if not station or len(station) == 0:
                    station = None
                else:
                    station = station[0]
                    if kwargs["level"] != None:
                        station.level = kwargs["level"]
                        station.save()
            except:
                pass

            if not station:
                try:
                    station = Station(**kwargs)
                    if station:
                        station.save()
                    else:
                        implError = True
                except:
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError() 
        else:
            return Response({'id': station.id})

    def put(self, request, format=None):
        badRequest = False
        implError = False
        notFound = False
        hasName = False
        hasLevel = False

        data = json.loads(request.body)
        try:
            id = data["id"]
        except:
            badRequest = True

        try:
            name = data["name"]
            hasName = True
        except:
            pass

        try:
            level = data["level"]
            hasLevel = True
        except:
            pass

        if not hasLevel and not hasName:
            badRequest = True

        if not badRequest:
            station = None

            # see if the station already exists

            try:
                station = Station.objects.filter(id=id)
                if not station or len(station) == 0:
                    station = None
                else:
                    station = station[0]
            except:
                pass

            if not station:
                notFound = True 
            else:
                try:
                    if hasName:
                        station.name=name
                    if hasLevel:
                        station.level=level
                    station.save()
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
        
    def delete(self, request, station_id=None, format=None):
        station = None

        # see if the station exists

        try:
            station = Station.objects.filter(id=station_id)
            if not station or len(station) == 0:
                station = None
            else:
                station = station[0]
        except:
            station = None

        if not station:
            raise NotFound
        else:
            station.delete()

        return Response({})
