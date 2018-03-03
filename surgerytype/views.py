# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from surgerytype.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

import json
import sys

class SurgeryTypeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["name"] = entry.name
        return m

    def get(self, request, surgery_type_id=None, format=None):   
        badRequest = False
        notFound = False
        surgery_type = None
        if surgery_type_id:
            try:
                surgery_type = SurgeryType.objects.get(id = surgery_type_id)
                ret = self.serialize(surgery_type)
            except:
                surgery_type = None
                notFound = True
        else: 
            try:
                sur = request.GET.get('name','')
            except:
                badRequest = True

            if not sur == '' and not badRequest:
                try:
                    surgery_type = SurgeryType.objects.get(name = sur)
                    ret = self.serialize(surgery_type)
                except:
                    surgery_type = None
                    notFound = True
            else:
                ret = []
                for x in SurgeryType.objects.all():
                    ret.append(self.serialize(x))

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
                if SurgeryType.objects.all().filter(name = data['name']).exists():
                    badRequest = True
            except:
                implMsg = "SurgeryType.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                surgery_type = SurgeryType(**data)
                if surgery_type:
                    surgery_type.save()
                else:
                    implMsg = "Unable to create surgery_type"
                    implError = True
            except:
                implMsg = "SurgeryType create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':surgery_type.id})

    def delete(self, request, surgery_type_id = None, format = None):
        surgery_type = None
        try:
            surgery_type = SurgeryType.objects.get(id = surgery_type_id)
        except:
            surgery_type = None
        if not surgery_type:
            raise NotFound
        else:
            surgery_type.delete()
        return Response({})
