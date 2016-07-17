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
from patient.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

class PatientView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, patient_id=None, format=None):
        patient = None
        if patient_id:
            try:
                patient = Patient.objects.filter(id = patient_id)
            except:
                patient = None
        else:
            try:
                patient = Patient.objects.all()
            except:
                patient = None

        if not patient:
            raise NotFound
        else:
            ret = []
            for x in patient:
                m = {}
                m["paternal_last"] = x.paternal_last  
                m["maternal_last"] = x.maternal_last  
                m["first"] = x.first  
                m["middle"] = x.middle  
                m["suffix"] = x.suffix  
                m["prefix"] = x.prefix  
                m["dob"] = x.dob.strftime("%m/%d/%Y")
                m["gender"] = x.gender  
                m["id"] = x.id
                ret.append(m)
            return Response(ret)

    def put(self, request, format=None):
        badRequest = False
        implError = False
        notFound = False

        data = json.loads(request.body)
        try:
            id = data["id"]
        except:
            badRequest = True
        try:
            paternal_last = data["paternal_last"]
        except:
            badRequest = True
        try:
            maternal_last = data["maternal_last"]
        except:
            badRequest = True
        try:
            first = data["first"]
        except:
            badRequest = True
        try:
            middle = data["middle"]
        except:
            badRequest = True
        try:
            suffix = data["suffix"]
        except:
            badRequest = True
        try:
            prefix = data["prefix"]
        except:
            badRequest = True
        try:
            dob = data["dob"]
            dob = datetime.strptime(dob, "%m/%d/%Y")
        except:
            badRequest = True
        try:
            gender = data["gender"]
        except:
            badRequest = True

        if not badRequest:
            patient = None

            # see if the patient already exists

            try:
                patient = Patient.objects.filter(id=id)
                if not patient or len(patient) == 0:
                    patient = None
                else:
                    patient = patient[0]
            except:
                pass

            if not patient:
                notFound = True 
            else:
                try:
                    patient.paternal_last=paternal_last
                    patient.maternal_last=maternal_last
                    patient.first=first
                    patient.middle=middle
                    patient.suffix=suffix
                    patient.prefix=prefix
                    patient.dob=dob
                    patient.gender=gender
                    patient.save()
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
        
    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            paternal_last = data["paternal_last"]
        except:
            badRequest = True
        try:
            maternal_last = data["maternal_last"]
        except:
            badRequest = True
        try:
            first = data["first"]
        except:
            badRequest = True
        try:
            middle = data["middle"]
        except:
            badRequest = True
        try:
            suffix = data["suffix"]
        except:
            badRequest = True
        try:
            prefix = data["prefix"]
        except:
            badRequest = True
        try:
            dob = data["dob"]
            dob = datetime.strptime(dob, "%m/%d/%Y")
        except:
            badRequest = True
        try:
            gender = data["gender"]
        except:
            badRequest = True

        if not badRequest:
            patient = None

            # see if the patient already exists

            try:
                patient = Patient.objects.filter(paternal_last=paternal_last,
                                                 maternal_last=maternal_last,
                                                 first=first,
                                                 middle=middle,
                                                 suffix=suffix,
                                                 prefix=prefix,
                                                 dob=dob,
                                                 gender=gender)
                if not patient or len(patient) == 0:
                    patient = None
                else:
                    patient = patient[0]
            except:
                implMsg = "Patient.objects.filter {} {}".format(sys.exc_info()[0], data)
                implError = True

            if not patient:
                try:
                    patient = Patient(paternal_last=paternal_last,
                                      maternal_last=maternal_last,
                                      first=first,
                                      middle=middle,
                                      suffix=suffix,
                                      prefix=prefix,
                                      dob=dob,
                                      gender=gender)
                    if patient:
                        patient.save()
                    else:
                        implMsg = "Unable to create patient"
                        implError = True
                except:
                    implMsg = "Patient create {} {}".format(sys.exc_info()[0], data)
                    implError = True
        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': patient.id})
        
    def delete(self, request, patient_id=None, format=None):
        patient = None

        # see if the patient exists

        try:
            patient = Patient.objects.filter(id=patient_id)
            if not patient or len(patient) == 0:
                patient = None
            else:
                patient = patient[0]

        except:
            patient = None

        if not patient:
            raise NotFound
        else:
            patient.delete()

        return Response({})
