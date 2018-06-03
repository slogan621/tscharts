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
from clinic.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import json

class ClinicView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @log_request
    def get(self, request, clinic_id=None, format=None):
        clinic = None
        date = None
        badRequest = False
        implError = False
        notFound = False

        if clinic_id:
            try:
                ret = {}
                clinic = Clinic.objects.get(id = clinic_id)
                if clinic:
                    try:
                        ret["id"] = clinic.id  
                        ret["start"] = clinic.start.strftime("%m/%d/%Y")
                        ret["end"] = clinic.end.strftime("%m/%d/%Y")  
                        ret["location"] = clinic.location
                    except:
                        implError = True
                else:
                    notFound = True
            except:
                notFound = True
        else:
            date = request.GET.get('date', '')
            if date:
                try:
                    date = datetime.strptime(date, "%m/%d/%Y")
                except:
                    badRequest = True
            else:
                date = None

            if not badRequest:
                try:
                    clinic = Clinic.objects.all()
                except:
                    implError = True

                if not implError and (not clinic or len(clinic) == 0):
                    notFound = True

            if not notFound and not implError and not badRequest:
                notFound = True
                ret = []
                for x in clinic:
                    if date:
                        if date.date() >= x.start and date.date() <= x.end:
                            ret = {}
                            ret["id"] = x.id  
                            ret["start"] = x.start.strftime("%m/%d/%Y")
                            ret["end"] = x.end.strftime("%m/%d/%Y")  
                            ret["location"] = x.location
                            notFound = False
                            break
                    else:
                        m = {}
                        m["id"] = x.id  
                        m["start"] = x.start.strftime("%m/%d/%Y")
                        m["end"] = x.end.strftime("%m/%d/%Y")  
                        m["location"] = x.location
                        notFound = False
                        ret.append(m)
        if notFound:
            return HttpResponseNotFound()
        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError() 
        return Response(ret)

    @log_request
    def post(self, request, format=None):

        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            location = data["location"]
        except:
            badRequest = True
        try:
            start = data["start"]
            start = datetime.strptime(start, "%m/%d/%Y")
        except:
            badRequest = True
        try:
            end = data["end"]
            end = datetime.strptime(end, "%m/%d/%Y")
        except:
            badRequest = True

        if not badRequest:
            clinic = None

            # see if the clinic already exists

            try:
                clinic = Clinic.objects.filter(location=location,
                                               start=start,
                                               end=end)
                if not clinic or len(clinic) == 0:
                    clinic = None
                else:
                    clinic = clinic[0]
            except:
                pass

            if not clinic:
                try:
                    clinic = Clinic(location=location, start=start, end=end)
                    if clinic:
                        clinic.save()
                    else:
                        implError = True
                except:
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError() 
        else:
            return Response({'id': clinic.id})
       
    @log_request 
    def delete(self, request, clinic_id=None, format=None):
        clinic = None

        # see if the clinic exists

        try:
            clinic = Clinic.objects.filter(id=clinic_id)
            if not clinic or len(clinic) == 0:
                clinic = None
            else:
                clinic = clinic[0]
        except:
            clinic = None

        if not clinic:
            raise NotFound
        else:
            clinic.delete()

        return Response({})
