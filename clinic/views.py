from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from clinic.models import *
from datetime import *
from django.core import serializers
import json

class ClinicView(APIView):

    '''
    All volunteers at specified clinic 
    Returns 404 if clinic not found
    Otherwise, 200 OK and (possibly empty) array of volunteers. 
    '''

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, clinic_id = None, format=None):
        clinic = None
        if clinic_id:
            try:
                clinic = Clinic.objects.filter(id = clinic_id)
                if clinic and len(clinic) > 0:
                    clinic = clinic[0]
            except:
                clinic = None
        else:
            try:
                clinic = Clinic.objects.all()
                if clinic and len(clinic) == 0:
                    clinic = None
            except:
                clinic = None

        if not clinic:
            raise NotFound
        else:
            resp = serializers.serialize("json", clinic)
            struct = json.loads(resp)
            return Response(struct)

        '''
    curl -X POST http://127.0.0.1:8000/badges/ -d '{"name": "Bob Chalfa",
"date": "November 2015", "job": "Inventory"}' -H 'Authorization: Token
9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
        '''

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
            start = datetime.datetime.strptime(start, "%m/%d/%Y")
        except:
            badRequest = True
        try:
            end = data["end"]
            end = datetime.datetime.strptime(start, "%m/%d/%Y")
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
            return Response({'id': clinic})
        
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
