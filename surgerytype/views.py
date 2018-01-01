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

class SurgerytypeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["name"] = entry.name
        return m

    def get(self, request, surgerytype_id=None, format=None):   
        badRequest = False
        notFound = False
        surgerytype = None
        if surgerytype_id:
            try:
                surgerytype = Surgerytype.objects.get(id = surgerytype_id)
                ret = self.serialize(surgerytype)
            except:
                surgerytype = None
                notFound = True
        else: 
            try:
                sur = request.GET.get('name','')
            except:
                badRequest = True

            if not sur == '' and not badRequest:
                try:
                    surgerytype = Surgerytype.objects.get(name = sur)
                    ret = self.serialize(surgerytype)
                except:
                    surgerytype = None
                    notFound = True
            else:
                ret = []
                for x in Surgerytype.objects.all():
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
                if Surgerytype.objects.all().filter(name = data['name']).exists():
                    badRequest = True
            except:
                implMsg = "Surgerytype.objects.all().filter {} {}".format(sys.exc_info()[0], data)
                implError = True

        if not badRequest and not implError:
            try:
                surgerytype = Surgerytype(**data)
                if surgerytype:
                    surgerytype.save()
                else:
                    implMsg = "Unable to create surgerytype"
                    implError = True
            except:
                implMsg = "Surgerytype create {} {}".format(sys.exc_info()[0], data)
                implError = True

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id':surgerytype.id})

    def delete(self, request, surgerytype_id = None, format = None):
        surgerytype = None
        try:
            surgerytype = Surgerytype.objects.get(id = surgerytype_id)
        except:
            surgerytype = None
        if not surgerytype:
            raise NotFound
        else:
            surgerytype.delete()
        return Response({})
