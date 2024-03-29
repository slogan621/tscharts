#(C) Copyright Xinyue Han 2017
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from medications.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

class MedicationsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["name"] = entry.name
        return m

    def get(self, request, medication_id=None, format=None):   
        badRequest = False
        notFound = False
        medication = None
       #If there is a medication id
        if medication_id:
            try:
                medication = Medications.objects.get(id = medication_id)
                ret = self.serialize(medication)
            except:
                medication = None
                notFound = True
        else: #If there is no medication id
            try:
                med = request.GET.get('name','')
            except:
                badRequest = True

            if not med == '' and not badRequest:
                try:
                    medication = Medications.objects.get(name = med)
                    ret = self.serialize(medication)
                except:
                    medication = None
                    notFound = True
            else:
                ret = []
                for x in Medications.objects.all():
                    ret.append(x.name)

        if badRequest:
            return HttpResponseBadRequest()
        elif notFound:
            return HttpResponseNotFound()
        else:
            return Response(ret)
    
    def post(self, request, format = None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        
        try:
            name = data['name']
            if len(name) == 0:
                badRequest = True
        except:
            badRequest = True

        if not badRequest:
            try:
                if Medications.objects.all().filter(name = data['name']).exists():
                    badRequest = True
            except:
                implMsg = "Medications.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                medication = Medications(**data)
                if medication:
                    medication.save()
                else:
                    implMsg = "Unable to create medication"
                    implError = True
            except:
                implMsg = "Medication create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':medication.id})

    def delete(self, request, medication_id = None, format = None):
        medication = None
        try:
            medication = Medications.objects.get(id = medication_id)
        except:
            medication = None
        if not medication:
            raise NotFound
        else:
            medication.delete()
        return Response({})
