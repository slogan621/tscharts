from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from clinic.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest

import json

class ClinicView(APIView):

    '''
    All volunteers at specified clinic 
    Returns 404 if clinic not found
    Otherwise, 200 OK and (possibly empty) array of volunteers. 
    '''

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, clinic_id=None, format=None):
        clinic = None
        if clinic_id:
            try:
                clinic = Clinic.objects.filter(id = clinic_id)
            except:
                clinic = None
        else:
            try:
                clinic = Clinic.objects.all()
            except:
                clinic = None

        if not clinic:
            raise NotFound
        else:
            ret = []
            for x in clinic:
                m = {}
                m["id"] = x.id  
                m["start"] = x.start  
                m["end"] = x.end  
                m["location"] = x.location
                ret.append(m)
            return Response(ret)

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

        return Response({})
