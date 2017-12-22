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
 

    def get(self, request, medication_id=None, format=None):
    
        badRequest = False
        notFound = False
        medication = None
       #If there is a medication id
        if medication_id:
            try:
                medication = Medications.objects.get(id = medication_id)
                ret = medication.name
            except:
                medication = None
        else:
            med = request.GET.get('medication','')
            if not med == '' and not badRequest:
                try:
                    medication = Medications.objects.filter(name = med)
                    ret = medication.id
                except:
                    medication = None
                    badRequest = True

        if not patient and not badRequest:
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
            return Response(ret) #get returns the whole list  filter(name = medication) 3 ways
    
    def post(self, request, format = None):
        badRequest = False
        implError = False

        data = json.loads(request.body)

        try:
            medication = Medications.objects.filter(name = data["medication"])
            if medication and len(medication)>0:
                badRequest = True
        except:
            implMsg = "Medication.objects.filter {} {}".format(sys.exc_info()[0], data)
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
            medication = Medications.objects.get(id=medication_id)
        except:
            medication = None
        if not medication:
            raise NotFound
        else:
            medication.delete()
        return Response({})
